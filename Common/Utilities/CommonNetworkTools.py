import time
from urllib2 import URLError

import pexpect

from Common.ConfigFiles import RestAPIConstants
from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.Utilities import SSHConnections
from Common.Utilities.Enums import DeploymentType
from Common.Utilities.Libs.retry import retry
from Common.Utilities.Libs_API.APIClient_SMSRest import SMSAPIClient
from Common.Utilities.Libs_API.API_Functions import APIWrapper
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.TestExceptions import FailedLoginError, DeploymentException
from Common.Utilities.UserWrapper import UserWrapper
from TestExecute.TestContext import Test_Context


@retry(exceptions=FailedLoginError, delay=15, tries=10)
def check_can_ssh_connect(ip_address, user=None, port=None):
    """
    This function is used to test if ssh connection can be established to DEVICE i.e. CMS or NTD ONLY.
    The wait times are cumulative of SSHConnection.create_connect(also uses retry) and pexpect time out (+30s pre try)

    Function does not return anything, if connection is established it returns control to wherever it was called from
    On failed attempt it'll throw FailedLoginError exception.
    :param port: 2024 or 2222
    :param user: object representing user
    :param ip_address: address of the device
    :return:
    """
    connection_details = ConfigLoader.get_general_config('DeviceConnectionDetails')
    if not user:
        user = UserWrapper(connection_details['User'],
                           connection_details['Password'],
                           None)

    if not port:
        port = get_pcli_port(ip_address)

    cli = SSHConnections.create_connect(user.name,
                                        user.password,
                                        ip_address,
                                        port)

    cli.sendline('show')
    index = cli.expect(['Management', 'syntax error', pexpect.TIMEOUT])
    if index in [0, 1]:  # either logged to pCLI where show works, or to CLI where it'll result in syntax error
        PrintMessage("Connection to {0} established, looking good!".format(ip_address))
        time.sleep(30)  # Adding sleep due to api check being currently unreliable (see SWALL-5198)
        return
    elif index == 2:
        PrintMessage("Failed to log onto - re-trying.")
        if type(cli.before) in [str, list] and len(cli.before) > 0:
            PrintMessage("__________________BEFORE__________________ \r\n {0}".format(cli.before))
        if type(cli.after) in [str, list] and len(cli.after) > 0:
            PrintMessage("___________________AFTER__________________ \r\n {0}".format(cli.after))

        raise FailedLoginError


@retry(exceptions=(DeploymentException, URLError), delay=5, tries=10)
def is_rest_api_service_up(api_client=None, cms_ip=None):
    """
    Currently unused but might come handy once SWALL-5198 is addressed
    :return:
    """
    if api_client is None:
        api_client = APIWrapper(SMSAPIClient(cms_ip))

    assert isinstance(api_client, APIWrapper)

    data = api_client.get_v1(RestAPIConstants.URL_HEALTH_STATUS, expected_http_code=[503, 200])

    if data and 'status' in data and data['status'] == 'UP':
        PrintMessage('CMS REST API HEALTH CHECK says its OK')
        return True
    else:
        PrintMessage('CMS REST API Service is not yet up')
        raise DeploymentException()


def get_cli_port(ip_address):
    """
    Method makes an attempt to figure out device type from given IP address
    This will return None for device type = gx as currently it does no uses port 2024
    :param ip_address:
    :return:
    """
    device_type = get_device_type_from_ip(ip_address)

    return Test_Context.connection_details['CLI_Port'] if device_type != DeploymentType.gx else None


def get_pcli_port(ip_address):
    """
    Method makes an attempt to figure out device type from given IP address
    This will return None for device type = gx as currently it does no uses port 2222
    :param ip_address:
    :return:
    """
    device_type = get_device_type_from_ip(ip_address)

    return Test_Context.connection_details['pCLI_Port'] if device_type != DeploymentType.gx else None


def get_device_type_from_ip(ip_address):
    """
    Method iterates through deployed device until match is found
    :param ip_address:
    :return: deployment type of found device or None if none is found
    """
    deployed_devices = Test_Context.deployed_devices
    for device_name in deployed_devices:
        device = deployed_devices[device_name]
        if device.ip_address == ip_address:
            return device.deployment_type
    return None