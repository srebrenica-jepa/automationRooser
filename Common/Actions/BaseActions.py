import time
import traceback
from urllib2 import URLError

from Common.ConfigFiles import RestAPIConstants
from Common.Utilities import SSHConnections, PExpectWrapper
from Common.Utilities.Enums import UsersChoice, DeviceStatus
from Common.Utilities.Libs.retry import retry
from Common.Utilities.Libs_API.APIClient_SMSRest import SMSAPIClient, APIError
from Common.Utilities.Libs_API.API_Functions import APIWrapper
from Common.Utilities.Logging import PrintMessage, LoggingLevel
from Common.Utilities.TestExceptions import CLINoResults, DeploymentException

# DEVICE IN SYNC
WAIT_FOR_NTD = "wait_for_ntd> Waiting for device to sync with SMS after initial deployment."
WAIT_FOR_NTD_DEPLOYED = '{0} device deployed but not required to be in sync (deploymentState:"{1}", ' \
                        'connectionState:"{2}", deploymentAction:"{3}"), done.'
WAIT_FOR_NTD_RE_TRY = '{0} device not ready (deploymentState:"{1}", connectionState:"{2}", ' \
                      'deploymentAction:"{3}"), re-try: {4}'
WAIT_FOR_NTD_IN_SYNC = '{0} device deployed and in-synced (deploymentState:"{1}", connectionState:"{2}", ' \
                       'deploymentAction:"{3}"), done.'

# SMS CLI constants
CONF_MODE = 'conf'
COMMIT_CHANGES = 'commit'
EXIT_CONF = 'exit'
SHOW_HISTORY = 'show cli history {0}'
SUCCESSFUL_COMMIT = ['Commit complete', 'No modifications to commit.']

SHOW_DEFAULT_XPATH = ' | details | nomore | display xpath'
SHOW_JSON = ' | nomore | display json'
SHOW_DETAILS = ' | details'

REQUEST_DEVICE_SYNC = 'request devices device {0} sync-to-device'
SET_PROTECTION_PROFILE = 'set policy protection-profile {0} '


class BaseActionsCLI(object):
    cli_prompt = None
    delaybeforesend = 0.3

    def __init__(self, user, host, port=None, timeout=30):
        self.user = user
        self.host = host
        self.port = port
        self.timeout = timeout
        self._cli = None

    def __del__(self):
        self.close_connection()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_connection()

    def close_connection(self):
        if self._cli is not None:
            self._cli.close()
            self._cli = None

    @property
    def cli(self):
        if self._cli is None:
            self._connect()
        return self._cli

    def _connect(self):
        self._cli = SSHConnections.create_connect(self.user.name,
                                                  self.user.password,
                                                  self.host,
                                                  self.port,
                                                  expect=self.cli_prompt,
                                                  timeout=self.timeout,
                                                  delaybeforesend=self.delaybeforesend)
        time.sleep(2)

    #
    # Method responsible for executing the cli commands, with check if command did execute i.e. ok was printed
    # Not always handy to use it as expect command affects buffer content i.e. (before / after)
    # Each PExpect sendline() must be followed with expect otherwise not all commands are actually executed
    #

    def send_cmd(self, command_line='', expected_value=None, delay=None):
        """
        Wrapper around PExpect sendline command

        :param command_line:
        :param expected_value: Often used to reset position in pexpect buffer stream.
        :param delay: wait after sending command
        :return:
        """
        PrintMessage("cmd({0}): {1}".format(self.user.name, command_line))
        self.cli.sendline(command_line)

        if delay is not None:
            time.sleep(delay)

        if expected_value is not None:
            try:
                return self.cli.expect_exact(expected_value)
            except:
                PExpectWrapper.display_before_n_after(self.cli)
                raise

        return self.cli.before

    def expect(self, expect_value):
        try:
            PrintMessage("Expect value: {0}".format(expect_value))
            return self.cli.expect(expect_value)

        except:
            PExpectWrapper.display_before_n_after(self.cli)
            raise


class CMSBaseActionsCLI(BaseActionsCLI):
    def __init__(self, user, host, port=None, timeout=60):
        super(CMSBaseActionsCLI, self).__init__(user, host, port, timeout)

        self.api_client = APIWrapper(SMSAPIClient(host, sms_user=user))

    def _turn_on_config_mode(self):
        """
        This is only applicable to CMS connection.
        :return:
        """
        # previously executed test might have been stuck in conf mode
        # code belows attempts to fix the situation
        try:
            self.send_cmd(command_line=' ', expected_value=None)
            self.send_cmd(CONF_MODE)
        except:
            command_history_count = 15
            show_history = SHOW_HISTORY.format(command_history_count)

            PrintMessage('Uncommitted changes found, quiting configuration mode.')
            PrintMessage('Print history of last {0}-commands in configuration mode'.format(command_history_count))
            self.send_cmd(show_history, expected_value=show_history)

            self.send_cmd(EXIT_CONF)
            if PExpectWrapper.expect(self.cli, 'There are uncommitted changes.'):
                self.send_cmd(UsersChoice.yes)
                self.send_cmd(CONF_MODE)

            PrintMessage('Print history of last {0}-commands out of configuration mode'.format(command_history_count))
            self.send_cmd(show_history, expected_value=show_history)

    #
    # Method responsible for executing the cli commands, with check if command did execute i.e. ok was printed
    # Not always handy to use it as expect command affects buffer content i.e. (before / after)
    # Each PExpect sendline() must be followed with expect otherwise not all commands are actually executed
    #

    def send_cmd(self, command_line='', expected_value="[ok]", delay=None):
        """
        Wrapper around PExpect sendline command

        :param command_line:
        :param expected_value: by default it expects an [ok] string, this is tuned towards CMS communication
        However, this can be used by any ssh type connection
        :param delay: wait after sending command
        :return:
        """
        PrintMessage("cmd({0}): {1}".format(self.user.name, command_line))
        self.cli.sendline(command_line)

        if delay is not None:
            time.sleep(delay)

        if expected_value is not None:
            try:
                if '[error]' in self.cli.before:
                    PrintMessage('ERROR noted in cli', LoggingLevel.warning)
                    PExpectWrapper.display_before_n_after(self.cli)

                index = self.cli.expect(expected_value)
                if '[error]' in self.cli.before:
                    PrintMessage('ERROR noted in cli', LoggingLevel.warning)
                    PExpectWrapper.display_before_n_after(self.cli)

                return index

            except:
                PExpectWrapper.display_before_n_after(self.cli)
                raise

        return self.cli.before

    #
    # Method responsible for executing multiple cli commands in conf mode
    # populates commands with the protection profile name
    # Method auto-populates PROTECTION - PROFILE
    #

    def send_cmd_in_conf_mode(self,
                              commands,
                              expected_on_commit=SUCCESSFUL_COMMIT,
                              expect_on_each_command="[ok]",
                              check_pending_commits=True):
        if type(commands) != list:
            commands = [commands]

        self._turn_on_config_mode()
        for command in commands:
            self.send_cmd(command, expect_on_each_command)

        self.send_cmd(COMMIT_CHANGES, expected_value=expected_on_commit)
        cli_output = self.cli.buffer
        pexpect_index = self.send_cmd(EXIT_CONF, expected_value=['ok', 'There are uncommitted changes'])

        # If commit is not expected to be successful, allow quiting it without saving
        if expected_on_commit != SUCCESSFUL_COMMIT and expected_on_commit is not None and pexpect_index == 1:
            self.send_cmd(UsersChoice.yes, expected_value=None)
            #  get value from buffer, error displayed after commit

        if check_pending_commits:
            self.wait_for_pending_commits()
        return cli_output

    @retry(exceptions=CLINoResults, delay=1, tries=60)
    def wait_for_pending_commits(self):
        self.send_cmd('show debug devices pending-commits', 'pending-commits')
        pending_commits = PExpectWrapper.get_int_after_value(self.cli, 'pending-commits')

        if pending_commits > 0:
            PrintMessage('Pending commits found!', level=LoggingLevel.warning)
            raise CLINoResults('Pending commits in progress')

    @retry(exceptions=(TypeError, CLINoResults), delay=1, tries=2)
    def get_json_data(self, command_line, delay=None, data_struct=None, show_details=False):
        """
        Sends command to cli and gets the json data formatted into dictionary
        :param data_struct: expected data format, almost like a schema check ;)
        Expected string type. Format:
        ['data']['corero-cms-system:system']['software']['installed']

        :param command_line: Command is expected to contain '| nomore | display json'
        :param delay: wait after sending command
        :param show_details: Adds ' | details' to the command line, if missing
        :return:
        """
        if show_details and SHOW_DETAILS not in command_line:
            command_line += SHOW_DETAILS

        if SHOW_JSON not in command_line:
            command_line += SHOW_JSON
        self.send_cmd(command_line, expected_value='json', delay=delay)

        json_data = PExpectWrapper.get_json_from_cli(self.cli)

        if data_struct:
            try:
                return eval(str(json_data) + data_struct)
            except (TypeError, KeyError):
                PExpectWrapper.display_before_n_after(self.cli)
                return None

        return json_data

    def get_current_config_values(self, command_line, expected_value='xpath'):
        """
        Since the json doesn't return default values (SWALL-5184)
        Assumes the key and value are separate with white space
        Assumes path in xpath is forward slash separated
        Last string (closest to vale) is used as key when returning data i.e.
        '/devices/cms-device-adv:advanced-settings/sflow/counter-record-interval 1000' as:
        {'counter-record-interval':1000}
        :return:
        """
        command_line += SHOW_DEFAULT_XPATH
        self.send_cmd(command_line, expected_value=expected_value)
        all_data = PExpectWrapper.get_lines(self.cli, terminating_value='[ok]')

        result_data = {}
        for data in all_data:
            keys, value = data.split(' ')
            key = keys.split('/')
            key = key[len(key)-1]
            result_data[key] = value

        return result_data

    def setup_rule_thresholds(self,
                              rule_config,
                              test_settings,
                              protection_profile='ProtectionProfile',
                              expected_on_commit=SUCCESSFUL_COMMIT,
                              expect_on_command='[ok]',
                              delay=0):
        """
        Sets up rule thresholds for given instructions
        expected format: path_to_rule_settings %s (value to set)
        Method uses send_cmd_in_conf_mode where
        PROTECTION - PROFILE is auto populated
        :param delay: give a moment post posting configuration
        :param expect_on_command:
        :param expected_on_commit:
        :param rule_config:
        :param test_settings:
        :param protection_profile: default value: ProtectionProfile
        :return:
        """
        if protection_profile:
            set_defense_protection_profile = SET_PROTECTION_PROFILE.format(protection_profile)
        else:
            set_defense_protection_profile = SET_PROTECTION_PROFILE

        commands = []
        for optionString in test_settings.keys():
            option_commands = rule_config[optionString]
            value_to_set = test_settings[optionString]
            if not isinstance(value_to_set, list):
                value_to_set = [value_to_set]
            commands += [set_defense_protection_profile + option_commands.format(k) for k in value_to_set]

        self.send_cmd_in_conf_mode(commands,
                                   expected_on_commit=expected_on_commit,
                                   expect_on_each_command=expect_on_command)
        time.sleep(delay)  # wait after applying configuration

    def wait_for_ntd(self,
                     device_name,
                     max_try=50,
                     sync_expected=True,
                     expected_connection_state=DeviceStatus.ConnectionState.connected,
                     expected_deployment_state=DeviceStatus.DeploymentState.in_sync):
        PrintMessage(WAIT_FOR_NTD)

        re_try = 0
        while re_try < max_try:
            time.sleep(4)
            re_try += 1

            try:
                device_status = self.api_client.get_v1(RestAPIConstants.URL_DEVICE_STATUS.format(device_name))
            except (APIError, URLError) as e:
                tb = traceback.format_exc()
                PrintMessage('Encountered exception {0}, with args {1}'.format(type(e), e.args))
                PrintMessage(str(e))
                PrintMessage("Traceback: {0}".format(tb))
                continue

            if not sync_expected:
                if expected_connection_state == device_status['connectionState'] \
                        and DeviceStatus.DeploymentAction.none == device_status['deploymentAction']:
                    PrintMessage(WAIT_FOR_NTD_DEPLOYED.format(device_name,
                                                              device_status['deploymentState'],
                                                              device_status['connectionState'],
                                                              device_status['deploymentAction']))
                    return True

            if DeviceStatus.DeploymentState.sync_required in device_status['deploymentState']:
                PrintMessage('Attempt to sync device')
                self.send_cmd(REQUEST_DEVICE_SYNC.format(device_name))

            if expected_deployment_state == device_status['deploymentState'] \
                    and expected_connection_state == device_status['connectionState'] \
                    and DeviceStatus.DeploymentAction.none == device_status['deploymentAction']:
                PrintMessage(WAIT_FOR_NTD_IN_SYNC.format(device_name,
                                                         device_status['deploymentState'],
                                                         device_status['connectionState'],
                                                         device_status['deploymentAction']))
                return True

            PrintMessage(WAIT_FOR_NTD_RE_TRY.format(device_name,
                                                    device_status['deploymentState'],
                                                    device_status['connectionState'],
                                                    device_status['deploymentAction'],
                                                    re_try))

        if re_try == max_try:
            raise DeploymentException('Device is not yet in sync!')