#!/usr/bin/env python

import time
from re import search as re_search

import pexpect

from Common.Actions.ActionsShell import ActionsShell
from Common.Utilities import FileTools
from Common.Utilities.DeploymentUtils import DeploymentConstants as DepConst, InstallationPackageHandling
from Common.Utilities.Libs.retry.api import retry
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.TestExceptions import DeploymentException
from Common.Utilities.Version import Version
from Common.ConfigFiles.ConfigLoader import ConfigLoader
from TestHelpers import StringMethods

# Const
START_PROCESS = 'start corero/{0}'
STOP_PROCESS = 'stop {0}'


class LannerDeviceDeploy(object):
    shell = None
    temp_folder = None

    def __del__(self):
        # remove temp folder
        if self.temp_folder:
            PrintMessage('Delete temp folder: {0}'.format(self.temp_folder))
            self.shell.send_cmd('rm {0} -rd'.format(self.temp_folder))
            time.sleep(2)

    def log_as_support(self, device_name):
        deployment_config = ConfigLoader.get_test_run_config("Deployment_Values")
        device_ip_address = deployment_config[device_name]["IP_ADDRESS"]

        self.shell = ActionsShell(device_ip_address)

    def _copy_tar_file(self, build_number, ntd_release_version):
        version_to_deploy = Version(ntd_release_version)
        version_to_deploy.build = build_number
        herc_machine = ConfigLoader.get_deployment_config("Test_Machine")

        package_path = InstallationPackageHandling.get_intd_package_path_ips(version_to_deploy,
                                                                             tar_file=True)
        FileTools.copy_file_to_remote_location_scp(self.shell, package_path, herc_machine)

        # splitting path by slash and getting last part - file name
        package_name = package_path.split('/')[-1]

        return package_name

    def get_current_running_ntd1100_process(self):
        """
        Makes an attempt to retrieve currently running version. If nothing runs, None is returned.
        None value needs to be handled higher up.
        :return:
        """
        # reset pexpect buffer
        rand_str = StringMethods.get_unique_string()
        self.shell.send_cmd(rand_str, expected_value=rand_str)  # reset pexpect buffer location

        self.shell.send_cmd('initctl list | grep corero | grep running')
        index = self.shell.cli.expect([DepConst.iNTD_VERSION_RE_EXPECT, pexpect.TIMEOUT])
        if index == 0:
            running_version = self.shell.cli.after
            PrintMessage('Running iNTD version found: {0}'.format(running_version))
            return running_version
        else:
            return None

    def get_currently_running_ntd1100_version(self, current_process=None):
        """
        :return: version number i.e. 9.0.1.6666
        """
        if not current_process:
            current_process = self.get_current_running_ntd1100_process()

        if current_process:
            return re_search(DepConst.iNTD_VERSION_RE, current_process).group(1)
        return None

    @retry(exceptions=DeploymentException, delay=5, tries=5)
    def kick_start_ntd1100(self, process_name_to_start):
        currently_running_process = self.get_current_running_ntd1100_process()

        currently_running_ntd = self.get_currently_running_ntd1100_version(currently_running_process)
        if currently_running_ntd and process_name_to_start not in currently_running_ntd:
            self.shell.send_cmd(STOP_PROCESS.format(currently_running_process), delay=10)

        self.shell.send_cmd(START_PROCESS.format(process_name_to_start), delay=20)

        currently_running_process = self.get_current_running_ntd1100_process()
        if currently_running_process is None or process_name_to_start not in currently_running_process:
            raise DeploymentException('Expected ntd1100 version not running.')

        PrintMessage('Installed iNTD version: {0}'.format(process_name_to_start))

    def _install_from_tar(self, device_to_deploy, ntd_release_version):
        ntd_release_version_re = DepConst.iNTD_VERSION.format(ntd_release_version)
        tar_file = self._copy_tar_file(device_to_deploy.version.build, ntd_release_version)
        self.shell.send_cmd('tar -xf {0}'.format(tar_file))
        FileTools.is_remote_file_present_in_current_folder(self.shell, 'ddp-install.sh')

        self.shell.send_cmd('./ddp-install.sh', delay=30)
        self.shell.cli.expect(ntd_release_version_re)
        process_name_to_start = self.shell.cli.after

        self.kick_start_ntd1100(process_name_to_start)

        return process_name_to_start

    def verify_installed_version(self, installed_version):
        current_running = self.get_current_running_ntd1100_process()

        assert installed_version in current_running, "actual: {0}, expected: {1}".format(current_running,
                                                                                         installed_version)

    def deploy(self, device_to_deploy):
        assert device_to_deploy.version.build is not None

        self.log_as_support(device_to_deploy.name)
        current_running_process = self.get_current_running_ntd1100_process()
        current_running_version = self.get_currently_running_ntd1100_version(current_running_process)
        ntd_release_version = device_to_deploy.version.release_version

        if current_running_process is not None \
                and str(device_to_deploy.version.build) in current_running_version \
                and ntd_release_version in current_running_process:

            PrintMessage(DepConst.DEVICE_ALREADY_DEPLOYED.format(device_to_deploy.name,
                                                                 device_to_deploy.version.build))
            return device_to_deploy

        self.temp_folder = FileTools.create_remote_temp_folder(self.shell)
        installed_version = self._install_from_tar(device_to_deploy, ntd_release_version)
        self.verify_installed_version(installed_version)

        return device_to_deploy
