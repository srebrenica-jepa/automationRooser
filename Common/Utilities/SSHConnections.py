#!/usr/bin/env python
import pexpect

import Common.Utilities.Enums
from Common.Utilities import PExpectWrapper
from Common.Utilities.Libs.retry.api import retry
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.TestExceptions import FailedLoginError


@retry(exceptions=(FailedLoginError, pexpect.EOF), delay=10, tries=6)
def create_connect(user, password, host, port=None, expect=None, timeout=30, delaybeforesend=0.5):
    my_spawn = MyPExpectSpawn(timeout, delaybeforesend)
    my_spawn.log_with_ssh(user, password, host, port, expect)
    return my_spawn


class MyPExpectSpawn(pexpect.spawn):
    def __init__(self, timeout=30, delaybeforesend=0.5, logfile=None):
        pexpect.spawn.__init__(self,
                               None,
                               timeout=timeout,
                               maxread=2000,
                               searchwindowsize=None,
                               logfile=logfile,
                               cwd=None,
                               env=None)

        self.delaybeforesend = delaybeforesend

        self.username = None
        self.host = None
        self.port = None

    @staticmethod
    def remove_known_host_entry(host, port):
        """Method used to remove current entry from known_host file,
        this step is required to ensure smooth connection process without errors."""

        if port is not None:
            remove_host_command = "ssh-keygen -R [%s]:%s" % (host, port)
        else:
            remove_host_command = "ssh-keygen -R %s" % host

        local_cmd = pexpect.spawn(remove_host_command)

        if local_cmd.expect("known_hosts") != 0:
            print "known_hosts file wasn't updated - ssh log in might fail"
            return 1

        return 0

    @staticmethod
    def get_connection_string(user, host, port):
        """ Create ssh connection string
        this method bypasses the authentication file i.e. skips prompts if host is new or modified"""

        if port is not None:
            port_string = "-p {0}".format(port)
        else:
            port_string = ""

        option_strict_checking = '-o StrictHostKeyChecking=no'
        option_preferred_auth = '-o PreferredAuthentications=keyboard-interactive,password'
        option_pubkey_auth = '-o PubkeyAuthentication=no'
        credentials = "{0}@{1} {2}".format(user, host, port_string)

        return "ssh {0} {1} {2} {3}".format(option_strict_checking,
                                            option_preferred_auth,
                                            option_pubkey_auth,
                                            credentials)

    def log_with_ssh(self, username, password, host, port=None, expect=None):
        """
        Helper method used to login with SSH
        method removes host from known_host list
        method creates a connection string

        :param expect:
        :param username:
        :param password:
        :param host:
        :param port:
        :return:
        """
        PrintMessage("ssh-ing to {0}@{1}:{2}".format(username, host, port))
        self.username = username
        self.host = host
        self.port = port

        self.remove_known_host_entry(host, port)

        connection_string = self.get_connection_string(username, host, port)

        pexpect.spawn._spawn(self, connection_string)

        expect_at_connection = ["password",
                                "Failed to connect to server",
                                "Connection refused",
                                "No route to host",
                                pexpect.TIMEOUT,
                                pexpect.EOF]

        index = self.expect(expect_at_connection)

        if index == 0:
            if password:
                self.sendline(password)

            if expect:
                expect_ = [expect, pexpect.TIMEOUT, pexpect.EOF]
                index = self.expect(expect_)

                if index == 0:
                    return True
                else:
                    raise FailedLoginError

        else:
            PExpectWrapper.display_before_n_after(self)
            raise FailedLoginError

    def close_connection(self):
        """
        This sends exit to the remote shell. If there are stopped jobs then
        this automatically sends exit twice.
        :return:
        """

        try:
            self.sendline(Common.Utilities.Enums.ControlKeys.ctr_c)
            self.sendline("exit")
            index = self.expect([pexpect.EOF, "(?i)there are stopped jobs", pexpect.TIMEOUT])

            if index == 1:
                self.sendline("exit")
                self.expect(pexpect.EOF)
            elif index == 2:
                PExpectWrapper.display_before_n_after(self)
        except OSError:
            pass

        self.close()

        PrintMessage('Connection closed: {0}@{1}:{2}'.format(self.username, self.host, self.port))
