#!/usr/bin/env python
import json
import pexpect

from Common.Utilities.Libs.retry.api import retry
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.TestExceptions import CLINoResults
from Common.Utilities import Enums
from TestHelpers import StringMethods


# Shell
PROMPT_STATUS_CODE = 'echo status_$1code:$?'
RETURN_STATUS_CODE = 'status_code:'


def display_before_n_after(cli):
    if type(cli.before) in [str, list] and len(cli.before) > 0:
        PrintMessage("__________________BEFORE__________________ \r\n {0}".format(cli.before))
    if type(cli.after) in [str, list] and len(cli.after) > 0:
        PrintMessage("___________________AFTER__________________ \r\n {0}".format(cli.after))


@retry(exceptions=CLINoResults, delay=5, tries=2)
def get_line_from_buffer(cli):
    line = cli.readline()
    trimmed_line = line.strip()

    if len(trimmed_line) == 0:
        raise CLINoResults('No data read from buffer')

    return trimmed_line


@retry(exceptions=CLINoResults, delay=5, tries=2)
def get_text_after_value(cli, key, strip_value=None):
    message = "Get text after key {0} : {1}"
    index = cli.expect([key, '% No entries found.', pexpect.TIMEOUT])

    if index == 0:
        value = get_line_from_buffer(cli)
        PrintMessage(message.format(key, value))
        return value.strip(strip_value)
    elif index == 1:
        return None
    else:
        PrintMessage(message.format(key, '?? not found...'))
        raise CLINoResults(display_before_n_after(cli))


def get_int_after_value(cli, value):
    new_value = get_text_after_value(cli, value)

    if new_value is None:
        return 0
    else:
        return int(new_value)


def get_line_rvalue(cli, expected):
    try:
        for line in cli:
            stripped = line.rstrip()

            if expected not in stripped:
                continue

            index = stripped.index(expected)
            if stripped[index:index + len(expected)] == expected:
                matched = stripped[index + len(expected):].lstrip()
                PrintMessage('get_line_rvalue: {0}: {1}'.format(expected, matched))
                return matched

    except pexpect.TIMEOUT:
        display_before_n_after(cli)
        PrintMessage('get_line_rvalue: {0}: {1}'.format(expected, None))
        return None


def get_lines(cli, limit=None, terminating_value=None, set_buffer_tag=False):
    """
    Reads all the content from pexpect buffer and returns is back to the caller.
    Assumes all data searched for is already printed out to the output.
    :param set_buffer_tag: 
    :param terminating_value: 
    :param cli: pexpect handler to cli
    :param limit:  value to determine amount of data read, soft stop
    :return:
    """
    PrintMessage('get_lines executed')

    if set_buffer_tag:
        terminating_value = StringMethods.get_unique_string()
        cli.sendline(terminating_value)

    line_count = 0
    lines = []
    try:
        while True:
            line = cli.readline()
            stripped = line.rstrip()

            if terminating_value and terminating_value in stripped:
                break

            if len(stripped) > 0:
                lines.append(stripped)
                line_count += 1

            if limit and line_count >= limit:
                break

        return lines

    except pexpect.TIMEOUT:
        display_before_n_after(cli)
        return lines


def expect(cli, value, expected_index=0):
    try:
        return cli.expect(value) == expected_index

    except pexpect.TIMEOUT:
        display_before_n_after(cli)
        return False


def get_completions_in_conf_mode(cli, command):
    cli.sendline('conf')
    cli.sendline(command)
    cli.send("set \t")
    cli.send(Enums.ControlKeys.ctr_c)
    cli.expect('Possible completions:')

    return get_lines(cli, set_buffer_tag=True)


#
# Execute shell command and return status code
# Using bash non existing variable $1 to avoid issue with pexpect
# where the command send to CLI is also buffered
#
def execute_shell_command(cli, shell_command, expected_value=None):
    PrintMessage('Execute shell command: {0}'.format(shell_command))
    cli.sendline(shell_command)

    if expected_value:
        cli.expect(expected_value)

    cli.sendline(PROMPT_STATUS_CODE)
    cli.expect(RETURN_STATUS_CODE)

    return int(cli.readline())


class Decoder(json.JSONDecoder):
    """
    Courtesy of https://stackoverflow.com/questions/45068797/how-to-convert-string-int-json-into-real-int-with-json-loads
    """
    def decode(self, s, **kwargs):
        result = super(Decoder, self).decode(s)
        return self._decode(result)

    def _decode(self, o):
        if isinstance(o, str) or isinstance(o, unicode):
            try:
                return int(o)
            except ValueError:
                return o
        elif isinstance(o, dict):
            return {k: self._decode(v) for k, v in o.items()}
        elif isinstance(o, list):
            return [self._decode(v) for v in o]
        else:
            return o


def get_json_from_cli(cli):
    """
    preferably get smaller sets of json data as for some reason it chokes on json outputs with more than 30 lines
    for method to work correctly it is expected the display json part of command to be the last e.g.
    'show me the money | nomore | display json'
    :param cli:
    :return:
    """
    total_lines = ''
    try:
        while True:
            read_line = cli.readline().strip()

            if len(read_line) == 0 or read_line == '\x08':
                #  x08 character was found with print repr(string)
                #  this is an odd case, no idea how this got itself into CLI
                #  show configuration analytics message-controls
                continue

            if '*** ALARM' in read_line:
                #  Another odd case, CMS might throw an alarm at CLI while json scrubbing is taking place
                raise CLINoResults('CMS alarm invalidated json scrubbing')

            total_lines += read_line

            if total_lines.count('{') == total_lines.count('}') != 0:
                break

        cli_json = json.loads(total_lines, cls=Decoder)
        return cli_json
    except:
        PrintMessage('get_json_from_cli> failed to decode string: ' + total_lines)
        display_before_n_after(cli)


def get_user_groups(cms_action):
    """
    Returns user group of current user
    :param cms_action:
    :return:
    """
    cms_action.send_cmd('id', expected_value=None)

    # text content: '<group_tyoe>', gids=
    text = get_text_after_value(cms_action.cli, 'groups=')
    return [k for k in text.split(',') if 'cns-' in k]


def run_pexpect_command(command):
    PrintMessage("pexpect command: {0}".format(command))
    run_command_result = pexpect.run(command)
    PrintMessage("pexpect command result: {0}".format(run_command_result))

    return run_command_result
