#!/usr/bin/env python
import copy
import os
import shutil
import subprocess
import time
import zipfile

import Common.Utilities.DeploymentUtils.DeploymentHelper
from Common.Actions.ActionsProvisionalCLI import ActionsProvisionalCLI
from Common.Utilities import DiskTools, FileTools
from Common.Utilities.DeploymentUtils import DeploymentConstants
from Common.Utilities.Device import Device
from Common.Utilities.Enums import DeviceType
from Common.Utilities.Logging import PrintMessage
from Common.ConfigFiles.ConfigLoader import ConfigLoader
from TestHelpers import StringMethods
from ..VMware.TalkWithEsxServer import TalkWithESX


class VMWareSource(object):
    @staticmethod
    def _create_temp_folder():
        temp_folder = "/tmp/vm_unpacking_automation/{0}/".format(StringMethods.get_unique_string())
        PrintMessage("Create temp folder in: {0}".format(temp_folder))

        return DiskTools.create_folder(temp_folder)

    #
    # Function decides which of the source file is selected for deployment
    # ntd cores: 2 or 5, script will add -core to string to make matching with folder name more accurate
    # the KVM will never be deployed on VM - so skipping it all together
    #

    @staticmethod
    def _get_source_file(source_folder, device):
        file_extension = ".zip"

        try:
            folder_contents = [content for content in os.listdir(source_folder) if file_extension in content]
            folder_contents = filter(lambda x: 'kvm' not in x, folder_contents)

            PrintMessage("All files available: {0}".format(folder_contents))

            if device.device_type == DeviceType.ntd:
                core_count = str(device.deployment_config['Core_Count'])
                folder_contents = filter(lambda x: core_count + '-core' in x, folder_contents)

            PrintMessage("For device {0}, selected file: {1}".format(device.device_type, folder_contents))
        except TypeError:
            return None

        if len(folder_contents):
            return folder_contents[0]

        return None

    @staticmethod
    def _unzip_to_temp_folder(zip_file_name, source_folder):
        destination_folder = VMWareSource._create_temp_folder()

        with zipfile.ZipFile(source_folder + "/" + zip_file_name) as zip_file:
            zip_file.extractall(destination_folder)

        return destination_folder + os.path.splitext(zip_file_name)[0] + "/"

    # returns previous and existing build number
    @staticmethod
    def get_valid_previous_version(device):
        device_folder = ConfigLoader.get_test_run_config("Source_Values")["Device_Folder"]
        temp_device = copy.deepcopy(device)
        temp_device.version.build -= 1

        builds_to_traverse = 20
        safe_count = 0
        while safe_count < builds_to_traverse:
            safe_count += 1

            source_folder = FileTools.get_device_source_folder(temp_device, device_folder)
            source_file = VMWareSource._get_source_file(source_folder, device)

            if source_file:
                return temp_device.version

            temp_device.version.build -= 1

        return None

    #
    # Function returns folder to devices with set release type (class variable self.release_type)
    # self.device_type in [sms, ntd, swa]
    #

    def prep_source_files(self, device_to_deploy):
        device_folder = ConfigLoader.get_test_run_config("Source_Values")["Device_Folder"]
        source_folder = FileTools.get_device_source_folder(device_to_deploy,
                                                           device_folder)

        if source_folder is None:
            exception_message = "Haven't found any source files that match build number: {0}."
            raise Exception(exception_message.format(device_to_deploy.version.build))

        PrintMessage("Device found: {0}".format(source_folder))

        source_file = self._get_source_file(source_folder, device_to_deploy)

        if source_file is None:
            exception_message = "Failed to retrieve source file from: {0} for device: {1}"
            raise Exception(exception_message.format(source_file, device_to_deploy.device_type))

        build_number = Common.Utilities.DeploymentUtils.DeploymentHelper.get_build_version(source_file)
        PrintMessage("Extracted build number from zip file {0} > {1}".format(source_file, build_number))

        device_temp_folder = self._unzip_to_temp_folder(source_file, source_folder)
        PrintMessage("Source files dropped to temp folder: {0}".format(device_temp_folder))

        return build_number, device_temp_folder


class VMWareDeviceDeploy(object):
    def __init__(self):
        self._device = None

        self._ovf_file_path_to_temp = None
        self._test_run_config = ConfigLoader.get_test_run_config()
        self._day0_config_values = self._test_run_config.load("Day0_Values")

    def _get_formatted_day_zero_option_string(self, day0_key, day0_value):
        """self.day0_config_values[day0_key] is expected to be either a list or single item"""
        configuration_file_value = None
        try:
            configuration_file_value = self._day0_config_values[day0_key]
        except KeyError:
            print "modify_day_zero_file.get_formatted_day_zero_option_string(): " \
                  "Option in configuration file not found: " + day0_key

        if type(configuration_file_value) == list and len(configuration_file_value) > 1:
            return self._get_string_for_multiple_values(day0_value, configuration_file_value)
        elif type(configuration_file_value) == list:
            return day0_value.format(configuration_file_value[0])
        else:
            return day0_value.format(configuration_file_value)

    @staticmethod
    def _get_string_for_multiple_values(day0_value, configuration_file_value):
        template = "\n- {0}"
        populated_with_values = ""

        for value in configuration_file_value:
            populated_with_values += template.format(value)

        return day0_value.format(populated_with_values)

    def _modify_day_zero_file(self, device_temp_folder, device):
        os.chdir(device_temp_folder)
        day0cfg = device_temp_folder + "day0cfg"
        if not os.path.isfile(day0cfg + ".iso"):
            PrintMessage("No Day0.iso file found, skipping")
            return

        PrintMessage("Modifying Day0 file with with values from {0}".format(self._test_run_config.sourceFile))

        with open(day0cfg, "w") as my_file:
            my_file.write("---\n")
            my_file.write(DeploymentConstants.Day0_NEW_SETTING_IP_ADDRESS.format(device.ip_address))
            my_file.write(DeploymentConstants.Day0_NEW_SETTING_HOSTNAME.format(device.device_type))

            for key in DeploymentConstants.Day0_NEW_SETTINGS.keys():
                day_zero_option = self._get_formatted_day_zero_option_string(key,
                                                                             DeploymentConstants.Day0_NEW_SETTINGS[key])
                my_file.write(day_zero_option)

        self._update_iso_file()

    @staticmethod
    def _update_iso_file():
        PrintMessage("Update ISO file after modifying the Day0 configuration file.")

        with open("./script.sh", "wb") as my_file:
            for command in DeploymentConstants.Day0_ISO_UPDATE_COMMANDS:
                my_file.write(command + "\n")

        subprocess.call("chmod +x ./script.sh", shell=True)
        subprocess.call("./script.sh", shell=True)

    def _deploy_device(self, device):
        PrintMessage("Attempt to deploy the device to ESX server.")
        vmware_config_values = self._test_run_config.load("VMWare_Values")

        if self._ovf_file_path_to_temp is None:
            ova_file_name = "*.ovf"
        else:
            ova_file_name = self._ovf_file_path_to_temp

        management_network = '--net:Management="{0}"'.format(device.deployment_config["NET_Management"])
        if device.device_type == DeviceType.ntd:
            ovf_tool_command = DeploymentConstants.OVF_COMMAND.format(
                device.deployment_config["VM_Name"],
                vmware_config_values["Datastore"],
                management_network,
                '--net:External="{0}"'.format(device.deployment_config["NET_External"]),
                '--net:Internal="{0}"'.format(device.deployment_config["NET_Internal"]),
                ova_file_name,
                vmware_config_values["ESX_User"],
                vmware_config_values["ESX_Password"],
                vmware_config_values["Host"])
        elif device.device_type == DeviceType.sms:
            ovf_tool_command = DeploymentConstants.OVF_COMMAND.format(
                device.deployment_config["VM_Name"],
                vmware_config_values["Datastore"],
                management_network,
                '--net:Secondary="{0}"'.format(device.deployment_config["NET_Secondary"]),
                '',
                ova_file_name,
                vmware_config_values["ESX_User"],
                vmware_config_values["ESX_Password"],
                vmware_config_values["Host"])
        elif device.device_type == DeviceType.swa:
            ovf_tool_command = DeploymentConstants.OVF_COMMAND.format(
                device.deployment_config["VM_Name"],
                vmware_config_values["Datastore"],
                management_network,
                '--net:Secondary="{0}"'.format(device.deployment_config["NET_Secondary"]),
                '',
                ova_file_name,
                vmware_config_values["ESX_User"],
                vmware_config_values["ESX_Password"],
                vmware_config_values["Host"])
        else:
            raise BaseException("_deploy_device(): unexpected deviceType found: {0}".format(device.device_type))

        PrintMessage("OVF Command: {0}".format(ovf_tool_command))

        output = subprocess.check_output(ovf_tool_command, shell=True)
        PrintMessage('DeployDevices print output: {0}'.format(output))

    def _execute_deploy(self, device_to_deploy):
        TalkWithESX.switch_off_vm(device_to_deploy.ip_address)

        vm_source = VMWareSource()
        prepped_build_number, file_location = vm_source.prep_source_files(device_to_deploy)

        current_dir = os.getcwd()
        try:
            self._modify_day_zero_file(file_location, device_to_deploy)
            self._deploy_device(device_to_deploy)
        finally:
            os.chdir(current_dir)
            PrintMessage("Attempt to remove any device temp files at location {0}.".format(file_location))
            shutil.rmtree(file_location, ignore_errors=True)

        return prepped_build_number

    #
    # device_type - ntd, sms or swa
    # build_number - build number
    # core_count - 2 core, 4 core, kvm
    # device_name - NTD0 NTD1
    #

    def deploy(self, device_to_deploy):
        assert type(device_to_deploy) == Device

        # stored support password becomes obsolete with new device deployed
        ActionsProvisionalCLI.pop_password(device_to_deploy.ip_address)
        PrintMessage("Deploying device: {0}, with ip address: {1}, build number: {2}".format(
            device_to_deploy.name,
            device_to_deploy.ip_address,
            'latest' if device_to_deploy.version.build is None else device_to_deploy.version.build))

        done = False
        attempt_count = 0
        while not done:
            try:
                device_to_deploy.version.build = self._execute_deploy(device_to_deploy)

                done = True
            except subprocess.CalledProcessError, e:
                PrintMessage('DeployDevices error details: {0}'.format(e.output))
                PrintMessage('Attempting to re-try the deployment')

                time.sleep(10)
                attempt_count += 1
                if attempt_count > 5:
                    raise Exception('Failed to deploy device {0} at address {1}'.format(device_to_deploy.name,
                                                                                        device_to_deploy.ip_address))

        return device_to_deploy
