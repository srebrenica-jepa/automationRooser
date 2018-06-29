#!/usr/bin/env python
from re import search as re_search

from Common.Actions.BaseActions import BaseActionsCLI
from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.Utilities import FileTools, PExpectWrapper
from Common.Utilities.DeploymentUtils.KVM.VirshComm import VirshComm
from Common.Utilities.UserWrapper import UserWrapper


class KVMServer(BaseActionsCLI):
    def __init__(self):
        server_config = ConfigLoader.get_test_run_config("KVM_Server")
        self.user = UserWrapper(server_config['User'], server_config['Password'], None)

        super(KVMServer, self).__init__(self.user, server_config['Host'])
        self.delaybeforesend = 0.2

        self.virsh_comm = VirshComm(self)
        self.temp_folder = None

    def __del__(self):
        if self.temp_folder:
            self.send_cmd('rm {0} -rd -f'.format(self.temp_folder), delay=1)

        super(KVMServer, self).__del__()

    def send_cmd(self, command_line='', expected_value=None, delay=1):
        return super(KVMServer, self).send_cmd(command_line, expected_value, delay)

    def unzip_files(self, file_name):
        unzip_command = 'unzip -j {0}'.format(file_name)
        self.send_cmd(unzip_command, delay=10)

        show_files_command = 'ls -al'
        self.send_cmd(show_files_command)
        self.send_cmd('echo status_code:$?')
        output = PExpectWrapper.get_lines(self.cli, terminating_value='status_code:0')

        source_files_re = '([a-z-_0-9.]*\.qcow2)'
        source_files = []
        for output_line in output:
            source_file = re_search(source_files_re, output_line)
            if source_file and source_file.group(1):
                if source_file.group(1) in source_files:
                    continue

                source_files.append(source_file.group(1))

        return source_files

    def _replace_disks(self, disks_paths, qcow2_files):
        """
        Method replaces 'disks' files with newer version
        Assumptions are:
        1. local files have format similar to: *disk1.qcow2
        2. incoming files have format similar to: *disk1.qcow2
        :param disks_paths:
        :param qcow2_files:
        :return:
        """
        assert_message = "expected same amount of items, actual {0} and {1}".format(disks_paths, qcow2_files)
        assert len(disks_paths) == len(qcow2_files), assert_message

        for x in range(len(disks_paths)):
            disk_number = 'disk{0}'.format(x+1)

            source_file = [k for k in qcow2_files if disk_number in k][0]
            destination_file = [k for k in disks_paths if disk_number in k][0]

            self.send_cmd('mv -f {0} {1}'.format(source_file, destination_file), delay=3)

    def _copy_and_replace(self, device, source_path):
        disks_paths = self.virsh_comm.get_disk_paths(device.deployment_config['Domain_Name'])
        self.temp_folder = FileTools.create_remote_temp_folder(self)
        file_name = FileTools.copy_local_file_to_remote(source_path,
                                                        self.temp_folder,
                                                        self.host,
                                                        self.user.name,
                                                        self.user.password)

        qcow2_files = self.unzip_files(file_name)
        self._replace_disks(disks_paths, qcow2_files)

    def get_domain_state(self, domain_name):
        return self.virsh_comm.get_domain_state(domain_name)

    def update_disks_with_new(self, device, source_path):
        self.virsh_comm.turn_off_device(device.deployment_config['Domain_Name'])
        self._copy_and_replace(device, source_path)
        self.virsh_comm.turn_on_device(device.deployment_config['Domain_Name'])
