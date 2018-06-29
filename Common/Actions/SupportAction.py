#!/usr/bin/env python
import Common.Utilities.CommonNetworkTools
from Common.Actions.ActionsProvisionalCLI import ActionsProvisionalCLI
from Common.Actions.BaseActions import CMSBaseActionsCLI
from Common.Utilities import PExpectWrapper
from Common.Utilities.Enums import UserGroup, DeploymentType
from Common.Utilities.UserWrapper import UserWrapper
from TestExecute.TestContext import Test_Context


class SupportAction(CMSBaseActionsCLI):
    def __init__(self, host, port=None):
        if port is None:
            self.port = Common.Utilities.CommonNetworkTools.get_cli_port(host)
        else:
            self.port = port

        user = UserWrapper('support',
                           ActionsProvisionalCLI.get_password(host),
                           UserGroup.support)

        CMSBaseActionsCLI.__init__(self,
                                   user=user,
                                   host=host,
                                   port=self.port,
                                   timeout=60)

    def reset_support_password(self):
        self.user.password = ActionsProvisionalCLI.get_password(self.host)

    #
    # No comeback method - only to be used when executing it as a standalone script
    #
    def interact(self):
        self.send_cmd()
        self.cli.interact()

    def disable_all_rules(self, device_name):
        if not Test_Context.do_not_disable_all_rules:
            self.send_cmd(command_line='request debug disable-all-rules',
                          expected_value='Rules successfully disabled',
                          delay=1)

            if Test_Context.ntd_deployment_type == DeploymentType.gx:
                self.wait_for_ntd(device_name=device_name)

    def get_current_load_levels(self, protection_profile):
        show_queue_depth = 'show configuration policy protection-profile {0} advanced-settings ingress-load-level ' \
                           '| details'.format(protection_profile)
        self.send_cmd(show_queue_depth, show_queue_depth)

        queue_depth = {
            '0': '0',
            '1': PExpectWrapper.get_text_after_value(self.cli, 'level-1').strip(';'),
            '2': PExpectWrapper.get_text_after_value(self.cli, 'level-2').strip(';'),
            '3': PExpectWrapper.get_text_after_value(self.cli, 'level-3').strip(';'),
            '4': PExpectWrapper.get_text_after_value(self.cli, 'level-4').strip(';'),
            '5': PExpectWrapper.get_text_after_value(self.cli, 'level-5').strip(';'),
            '6': PExpectWrapper.get_text_after_value(self.cli, 'level-6').strip(';'),
            '7': PExpectWrapper.get_text_after_value(self.cli, 'level-7').strip(';'),
            '8': '-1'}

        return queue_depth

    def enable_logging_on_device(self, device_name):
        """
        Method expects to start from pCLI level
        :type device_name: object
        :return:
        """
        #  pretty logging
        self.send_cmd_in_conf_mode('set devices device {0} trace pretty'.format(device_name))

        #  temp to support iNTD issue with pending commits, print commits to device
        self.send_cmd_in_conf_mode('set java-vm java-logging logger com.corero.mgmt.core.template level level-all')

        # exit application CLI
        self.send_cmd('exit')
        self.enable_additional_logs_intd_investgation()

    def enable_additional_logs_intd_investgation(self):
        """
        As we do not know where currently
        :return:
        """
        #  Required to execute sed commands from shell level
        self.send_cmd('shell')

        try:
            #  temp to support iNTD issue with pending commits
            self.send_cmd('sed -ie "s/.*developer-log-level.*/ <developer-log-level>trace<\/developer-log-level>/" /opt/corero/cms/app/ncs.conf', delay=2)

            #  change log rotation
            self.send_cmd('sed -ie "s/10M/1G/" /etc/logrotate.d/cms', delay=2)
            self.send_cmd('/opt/corero/cms/tail-f/bin/ncs --reload', delay=10)

        finally:
            self.send_cmd('exit', delay=2)
