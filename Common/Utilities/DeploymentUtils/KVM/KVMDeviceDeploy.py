#!/usr/bin/env python
import os

import Common.Utilities.DeploymentUtils.DeploymentHelper
from Common.Actions.ActionsProvisionalCLI import ActionsProvisionalCLI
from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.Utilities import FileTools, PExpectWrapper
from Common.Utilities.DeploymentUtils.KVM.KVMServer import KVMServer
from Common.Utilities.Enums import DeviceType, KVMDeviceState
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.UserWrapper import UserWrapper
from Common.Utilities.Version import Version


class KVMDeviceDeploy(object):
    """
    Purpose of this class is to replace disks of an existing kvm device
    Source files are taken from Device_Folder (TestRunConfig): by default it is  /builds/vmbuild/release folder
    """

    def __init__(self):
        self.kvm_server = KVMServer()

    @staticmethod
    def _get_source_file(source_folder, device):
        """
        Makes an attempt to find specific file within the given folder.
        KVM deployment requires source file with 'kvm' within the name
        KVM deployment for NTD requires 'virtual-edition' string within the name

        :param source_folder:
        :param device:
        :return:
        """
        file_extension = ".zip"

        try:
            folder_contents = [content for content in os.listdir(source_folder) if file_extension in content]
            folder_contents = filter(lambda x: 'kvm' in x, folder_contents)

            PrintMessage("All files available: {0}".format(folder_contents))

            if device.device_type == DeviceType.ntd:
                folder_contents = filter(lambda x: 'virtual-edition' in x, folder_contents)

            PrintMessage("For device {0}, selected file: {1}".format(device.device_type, folder_contents))
        except TypeError:
            return None

        if len(folder_contents):
            return folder_contents[0]

        return None

    # @staticmethod
    # def get_valid_build_number(device, look_back=1):
    #     folder_build_number = None
    #     source_device_path = ConfigLoader.get_test_run_config("Source_Values")["Device_Folder"]
    #     while look_back > 0:
    #         source_folder = FileTools.get_device_source_folder(device.device_type,
    #                                                            folder_build_number,
    #                                                            source_device_path)
    #
    #         if source_folder is None:
    #             return None
    #
    #         source_file = KVMDeviceDeploy._get_source_file(source_folder, device)
    #         folder_build_number = StringMethods.get_build_version(source_folder)
    #         file_build_number = StringMethods.get_build_version(source_file)
    #
    #         if folder_build_number == file_build_number:
    #             return folder_build_number
    #
    #         folder_build_number -= 1
    #         look_back -= 1
    #
    #     return None

    def get_source_file_path(self, device):
        source_device_path = ConfigLoader.get_test_run_config("Source_Values")["Device_Folder"]
        source_folder_path = FileTools.get_device_source_folder(device,
                                                                source_device_path)
        source_file_name = self._get_source_file(source_folder_path, device)

        build_number = Common.Utilities.DeploymentUtils.DeploymentHelper.get_build_version(source_file_name)
        PrintMessage("Extracted build number from zip file {0} > {1}".format(source_file_name, build_number))

        return source_folder_path + '/' + source_file_name, build_number

    def _get_current_version(self, device_ip):
        connection_details = ConfigLoader.get_general_config('DeviceConnectionDetails')
        user = UserWrapper(connection_details["User"],
                           connection_details["Password"],
                           None)

        with ActionsProvisionalCLI(user, device_ip) as device_pcli_action:
            device_pcli_action.send_cmd('show version')
            device_version = PExpectWrapper.get_text_after_value(device_pcli_action.cli, 'Application Version : ')

        return Version(device_version)

    def deploy(self, device_to_deploy):
        """
        Implementation of this method is currently limited to replacing files used as disks on KVM server.
        
        Method is expected to:
        - Check if device exists
        - If exists and its online, check the version if same as expected - exit
        - If exists and its offline, replace disks with expected version
        - If doesn't exist bounce out with error

        device_name = domain_name
        :param device_to_deploy:
        :return:
        """

        domain_state = self.kvm_server.get_domain_state(device_to_deploy.deployment_config['Domain_Name'])

        if domain_state in [KVMDeviceState.online, KVMDeviceState.offline]:
            source_path, device_to_deploy.version.build = self.get_source_file_path(device_to_deploy)
            self.kvm_server.update_disks_with_new(device_to_deploy, source_path)
        else:
            raise Exception('unexpected device type')

        return device_to_deploy
