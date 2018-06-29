#!/usr/bin/env python

import pexpect

import Common.Utilities.CommonNetworkTools
from Common.Actions.BaseActions import BaseActionsCLI
from Common.Actions.SupportAction import SupportAction
from Common.Utilities import PExpectWrapper
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.UserWrapper import UserWrapper
from Common.Utilities.Version import Version
import Common.Utilities.Enums


# Action Support constants
NCS_CLI_PATH = '/opt/corero/{0}/tail-f/bin/ncs_cli -u support'.format(Common.Utilities.Enums.DeviceType.sms)
NCS_PATH = '/opt/corero/{0}/tail-f/bin/ncs_load'.format(Common.Utilities.Enums.DeviceType.sms)
SAVE_PROFILE = NCS_PATH + ' -WF p -P /{0}> {1}'
LOAD_PROFILE = NCS_PATH + ' -p /{0} -lm {1}'
CONFIG_FULL = '/tmp/init.state.all'
SXOS_FILE = '/corero/corero-linux'


class ActionsShell(BaseActionsCLI):
    """
    # Class responsible for extracting a support Token from SMS through CLI
    # By default shell is opened
    # Other methods expect to 'be' in the shell

    Class requires TestContext global populated
    """
    def __init__(self, host):
        super(ActionsShell, self).__init__(UserWrapper(None, None, None),
                                           host,
                                           Common.Utilities.CommonNetworkTools.get_pcli_port(host))

    def _connect(self):
        self.support_action = SupportAction(self.host, self.port)
        self.user = self.support_action.user
        self._cli = self.support_action.cli
        self._cli.sendline("shell")

    def _change_fire_wall_setup(self, service_action):
        firewall_set = False

        if self.cli.expect("vconsole") == 0:
            self.send_cmd("service iptables " + service_action)
            self.cli.expect("Redirecting")

            PrintMessage(self.cli.before)

            self.send_cmd("service iptables status")
            if service_action == "stop":
                firewall_set = self.cli.expect("(dead)") == 0
            else:
                firewall_set = self.cli.expect("(exited)") == 0

        return firewall_set

    def stop_fire_wall(self):
        return self._change_fire_wall_setup("stop")

    def start_fire_wall(self):
        return self._change_fire_wall_setup("start")

    # expected full command i.e. iptables -A INPUT -m state --state NEW -m tcp -p tcp --dport 8089 -j ACCEPT
    def open_iptables_port(self, command, expected):
        PrintMessage('Attempt to modify ip tables on {0}'.format(self.host))
        self.send_cmd('iptables -S')

        if self.cli.expect([expected, pexpect.TIMEOUT]) == 0:
            PrintMessage('IPTables already enabled - skipping')
            return

        if PExpectWrapper.execute_shell_command(self.cli, command) != 0:
            raise Exception('Failed opening ip tables!')

        if PExpectWrapper.execute_shell_command(self.cli, 'service iptables save', expected_value='[  OK  ]') != 0:
            raise Exception('Failed opening ip tables!')

    def tail_app_log(self):
        """no comeback method - only to be used when executing it as a standalone script"""
        if self.cli.expect("vconsole") == 0:
            self.send_cmd("tail -f /var/log/corero/app.log")

    def update_sxos_version(self, new_version):
        assert type(new_version) is Version
        new_version.verify()

        new_version_as_string = new_version.get_as_string(fill_with_zeros=0)

        linux_command = "echo '{0}' > {1}".format(new_version_as_string, SXOS_FILE)
        PrintMessage('Updating sxos version to {0}, with command: {1}'.format(new_version_as_string, linux_command))

        status_code = PExpectWrapper.execute_shell_command(self.cli, linux_command)

        if status_code == 0:
            PrintMessage('SXOS version was updated!')
        else:
            PrintMessage('Failed to update {0}, status code: {1}'.format(SXOS_FILE, status_code))

        # verify file is updated
        self.send_cmd('cat ' + SXOS_FILE)
        self.cli.expect(SXOS_FILE)
        self.cli.expect(new_version_as_string)

    #
    # used by get bug data to get dump of profile

    def save_all_profile(self, destination_file):
        save_dump = SAVE_PROFILE.format('', destination_file)
        status_code = PExpectWrapper.execute_shell_command(self.cli, save_dump)
        if status_code == 0:
            PrintMessage('Defense profile saved')
        else:
            PrintMessage('Failed to save Defense profile, status code: {0}'.format(status_code))
