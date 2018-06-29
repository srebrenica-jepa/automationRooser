#!/usr/bin/env python
from re import search as re_search

from Common.Actions.ActionsProvisionalCLI import ActionsProvisionalCLI
from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.Utilities import CommonNetworkTools
from Common.Utilities.DeploymentUtils.GX.GXDeviceDeploy import GXDeviceDeploy
from Common.Utilities.DeploymentUtils.KVM.KVMDeviceDeploy import KVMDeviceDeploy
from Common.Utilities.DeploymentUtils.Lanner.LannerDeviceDeploy import LannerDeviceDeploy
from Common.Utilities.DeploymentUtils.VMware.VMWareDeviceDeploy import VMWareDeviceDeploy
from Common.Utilities.Device import DeviceManager
from Common.Utilities.Enums import DeploymentType
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.UserWrapper import UserWrapper
from ConfigFiles import ConstantsCommands as Const
from TestExecute.TestContext import Test_Context


def deploy_with_deployer(deployer, device_to_deploy):
    """
    If no build number is supplied then most current version is used.
    This method makes sure all devices are deployed with matching build number.
    :param device_to_deploy:
    :param deployer:
    :return:
    """
    PrintMessage('Making an attempt to deploy device: {0}'.format(device_to_deploy.name))

    deployed_device = deployer.deploy(device_to_deploy)

    PrintMessage('Deployed device {0} with build number {1}.'.format(deployed_device.name,
                                                                     device_to_deploy.version.get_as_string()))

    return deployed_device


def deploy_devices(device_names, build_number_to_deploy=None):
    """
    Deploys ntd and sms VMs
    The build number is expected to be the same for both
    :param device_names:
    :param build_number_to_deploy:
    :return:
    """

    deployment_config = ConfigLoader.get_test_run_config('Deployment_Values')

    for device_name in device_names:
        device_to_deploy = DeviceManager.create_device_template_from_config(device_name)
        device_to_deploy.version.build = build_number_to_deploy

        device_deployment_type = deployment_config[device_name]['Deployment_Type']
        if device_deployment_type == DeploymentType.ntd1100:
            deployed_device = deploy_with_deployer(LannerDeviceDeploy(), device_to_deploy)
        elif device_deployment_type == DeploymentType.vmware:
            deployed_device = deploy_with_deployer(VMWareDeviceDeploy(), device_to_deploy)
        elif device_deployment_type == DeploymentType.kvm:
            deployed_device = deploy_with_deployer(KVMDeviceDeploy(), device_to_deploy)
        elif device_deployment_type == DeploymentType.gx:
            deployed_device = deploy_with_deployer(GXDeviceDeploy(), device_to_deploy)
        else:
            raise Exception("Unknown deployment type")

        Test_Context.deployed_devices[deployed_device.name] = deployed_device

        # this ensures, all subsequent devices are of the same build number
        build_number_to_deploy = deployed_device.version.build

    Test_Context.build_number = build_number_to_deploy

    connect_to_all_devices(device_names, deployment_config)

    PrintMessage('Initial deployment complete!')

    return Test_Context.build_number


def connect_to_all_devices(device_names, deployment_config):
    """
    Function will ensure that all devices can be connected through ssh
    :param device_names:
    :param deployment_config:
    :return:
    """
    PrintMessage("Make an attempt to connect to all deployed devices")
    for device_name in device_names:
        CommonNetworkTools.check_can_ssh_connect(Test_Context.deployed_devices[device_name].ip_address)

        deployment_type = deployment_config[device_name]['Deployment_Type']
        if device_name == Const.NTD_NAME_0 and deployment_type == DeploymentType.ntd1100:
            reboot_lanner_device(deployment_config[device_name]['IP_ADDRESS'])


def reboot_lanner_device(ip_address):
    """
    Reboot lanner device as per dev suggestion in SWALL-7668, SWALL-5845
    :return:
    """
    connection_details = ConfigLoader.get_general_config('DeviceConnectionDetails')
    user = UserWrapper(connection_details["User"],
                       connection_details["Password"],
                       None)

    with ActionsProvisionalCLI(user=user, host=ip_address) as admin_pcli:
        PrintMessage("Reboot lanner device -- as per SWALL-7668, SWALL-5845")
        admin_pcli.send_cmd("reboot", expected_value='This will reboot the device. Do you want to continue?')
        admin_pcli.send_cmd("y", expected_value='The system is going down for reboot NOW!')


def get_build_version(text):
    """
    Parses file name and returns build number
    :param text:
    :return:
    """
    if text is None:
        return None

    # odd case where version number for swa might be unset
    # instead of xxx-yyy have unset-yyy
    if 'unset' in text:
        reg_exp = '(\d+)'
    else:
        reg_exp = '\d.\d.\d.(\d+)'

    return int(re_search(reg_exp, text).group(1))