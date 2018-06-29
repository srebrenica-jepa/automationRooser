#!/usr/bin/env python
import re

import Common.Utilities.CommonNetworkTools
from Common.Actions.BaseActions import BaseActionsCLI
from Common.Utilities import PExpectWrapper
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.UserWrapper import UserWrapper
from TestExecute.TestContext import Test_Context


class ActionsProvisionalCLI(BaseActionsCLI):
    """
    Class manages connection to pCLI area and managing support password
    """
    _stored_passwords = {}

    def __init__(self, user, host, login_prompt='>'):
        """
        provisionalCLI, pCLI
        :param user:
        :param host:
        :param login_prompt:
        """
        super(ActionsProvisionalCLI, self).__init__(user=user,
                                                    host=host,
                                                    port=Common.Utilities.CommonNetworkTools.get_pcli_port(host),
                                                    timeout=60)
        self.cli_prompt = login_prompt
        self.delaybeforesend = 0.1

    def close_connection(self):
        if self._cli is not None:
            self.send_cmd('quit')
            self._cli.close()
            self._cli = None

    # delays added to work around NTD issue with long wait times when setting dns
    def setup_dns(self, dns_to_set='none', search_domain_to_set='none'):
        PrintMessage('Changing dns to {0}, search domain to {1} '.format(dns_to_set, search_domain_to_set))
        self.send_cmd('show dns')

        # # SWALL-1642, otherwise this if is not necessary
        # if PExpectWrapper.get_text_after_matched_value(self.cli, 'Error') is None:
        #     current_dns = PExpectWrapper.get_text_after_matched_value(self.cli, 'DNS Servers')
        #     current_search_domain = PExpectWrapper.get_text_after_matched_value(self.cli, 'DNS Search Domains')
        #
        #     if dns_to_set in current_dns and search_domain_to_set in current_search_domain:
        #         return

        self.send_cmd('setup dns')
        self.send_cmd()  # enter hostname

        self.send_cmd(dns_to_set)  # primary dns
        if dns_to_set != 'none':
            self.send_cmd('none')  # secondary dns

        self.send_cmd('none')  # dns domain
        self.send_cmd(search_domain_to_set)  # dns search domains

        if self.expect(['Enter \[A\]ccept', 'Enter \[C\]hange']) == 0:
            # save changes
            self.send_cmd('a', delay=10)
            self.expect('Applying changes...')
        else:
            # if no changes are introduced, exit without save
            self.send_cmd('e')

        self.send_cmd(delay=10)
        self.expect(self.cli_prompt)

    def setup_time(self, time_zone, enable_ntp='N', ntp_server=None):
        PrintMessage('Changing time zone to {0}, ntp server to {1} '.format(time_zone, ntp_server))

        self.send_cmd('setup time')
        self.send_cmd(enable_ntp)
        if enable_ntp.lower() == 'y':
            self.send_cmd(ntp_server)
            self.send_cmd('none')  # secondary server, none to finish server insertion

        self.send_cmd(time_zone)

        # expects [A]ccept, [C]hange
        if self.expect(['Enter \[A\]ccept', 'Enter \[C\]hange']) == 0:
            # save changes
            self.send_cmd('a', delay=60, expected_value='Applying changes...')
        else:
            # exit without saving as no modification was made
            self.send_cmd('e')

        # Added check to fish out any warnings SWALL-5007
        index = self.expect([self.cli_prompt, 'WARNING'])
        if index == 0:
            return
        elif index == 1:
            self.expect(self.cli_prompt)
            PrintMessage(PExpectWrapper.display_before_n_after(self.cli))
            assert False, "WARNING message is displayed: SWALL-5738"

    def disable_support_account(self):
        index = self.send_cmd('support-account status', expected_value=['Disabled', 'Enabled'])
        if index == 0:
            return True
        elif index == 1:
            self.send_cmd('support-account disable', expected_value=self.cli_prompt)
            ActionsProvisionalCLI.pop_password(self.host)

        return self.send_cmd('support-account status', expected_value=['Disabled', 'Enabled']) == 0

    def get_token(self):
        """
        Returns support token
        Support token is required to generate support account password

        # Process text [token = 1BYODOU7] to retrieve the token value i.e. 1BYODOU7
        :return:
        """
        self.send_cmd("support-account status")
        index = self.cli.expect(['Enabled', 'Disabled'])
        if index == 1:
            self.send_cmd("support-account enable")
            self.send_cmd("support-account status", expected_value='Support account status: Enabled')

        # required to fill pexpect buffer with string containing the token
        get_token_line_re = "token.*"
        get_token_re = "token:\s(.{8})"

        self.expect(get_token_line_re)
        token = re.search(get_token_re, self.cli.after).group(1)
        PrintMessage("Token value: {0}".format(token))

        return token

    # ---=== support password management ===---
    # ---=== those are class method by design, each new instantiated object must know about support password ===---

    @classmethod
    def get_password(cls, host_ip):
        if host_ip in cls._stored_passwords and cls._stored_passwords[host_ip]:
            PrintMessage("Using stored support password {0} for host {1}".
                         format(cls._stored_passwords[host_ip], host_ip))
        else:
            set_new_support_password(host_ip)

        return cls._stored_passwords[host_ip]

    @classmethod
    def store_password(cls, host_ip, support_password):
        cls._stored_passwords[host_ip] = support_password

    @classmethod
    def pop_password(cls, host_ip):
        if host_ip in cls._stored_passwords:
            return cls._stored_passwords.pop(host_ip)
        else:
            return None


def get_password_from_token(token):
    support_password = None
    user = UserWrapper(name="support", password=None, group=None)
    with BaseActionsCLI(user, host="cns-sss.corero-cns.com") as cns_action:
        if cns_action.cli.expect("Enter token:") != 0:
            raise Exception("SupportUserLogin > Failed retrieving token: {0}".format(token))

        cns_action.send_cmd(token)
        # .*Password: ([^\\r]*).*
        # (?<=Password: ).*?(?=\s)"

        # this will return two matches, two groups. Password is in the second group.
        if cns_action.cli.expect(".*Password: ([^\\r]*).*") != 0:
            PrintMessage("SupportUserLogin > Failed getting password")
            return

        support_password = cns_action.cli.match.group(1)

    PrintMessage('New support password: {0}'.format(support_password))

    return support_password


def set_new_support_password(host_ip):
    token = get_token(host_ip)
    password = get_password_from_token(token)

    PrintMessage("Password value: {0}".format(password))
    ActionsProvisionalCLI.store_password(host_ip, password)

    return password


def get_token(host_ip):
    admin_user = UserWrapper(Test_Context.connection_details['User'],
                             Test_Context.connection_details['Password'],
                             None)

    with ActionsProvisionalCLI(user=admin_user, host=host_ip) as admin_pcli:
        return admin_pcli.get_token()
