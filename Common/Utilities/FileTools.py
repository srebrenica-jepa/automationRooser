#!/usr/bin/env python
import os
import tempfile
import zipfile

import paramiko
import pexpect

from Common.Utilities import PExpectWrapper
from Common.Utilities.Libs.retry.api import retry
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.TestExceptions import CLINoResults


def unzip_to_temp_folder(zip_file_name, source_folder):
    destination_folder = tempfile.mkdtemp()

    with zipfile.ZipFile(source_folder + "/" + zip_file_name) as zip_file:
        zip_file.extractall(destination_folder)

    return destination_folder + os.path.splitext(zip_file_name)[0] + "/"


def create_remote_temp_folder(cmd):
    cmd.send_cmd('mktemp -d', delay=1)
    temp_folder = '/tmp/tmp{0}/'.format(PExpectWrapper.get_text_after_value(cmd.cli, '/tmp/tmp'))
    cmd.send_cmd('cd {0}'.format(temp_folder), delay=1)

    return temp_folder


@retry(exceptions=CLINoResults, delay=3, tries=4)
def is_remote_file_present_in_current_folder(cmd, file_name):
    """
    Method depends on pexpect timout delay
    :param cmd:
    :param file_name:
    :return:
    """
    PrintMessage('Attempt to find file: {0}'.format(file_name))
    index = cmd.send_cmd('ls -l', expected_value=[file_name, 'total 0', pexpect.EOF], delay=2)

    if index == 0:  # expect file_name
        return
    else:
        PrintMessage("Expected file not found, buffer content: \n {0}".format(cmd.cli.before))
        error_message = 'cli ls, file {0} not found'.format(file_name)
        raise CLINoResults(error_message)


def get_device_source_folder(device, source_device_path):
    """
    Assumption is source files are in /path/<device_type>/some mix of device_type and version_number
    :param device:
    :param source_device_path:
    :return:
    """
    path = source_device_path + "{0}/".format(device.device_type)
    folder_version_number = '_' + device.version.release_version
    device_folders = [path + f for f in os.listdir(path) if device.device_type in f and folder_version_number in f]

    if device.version.build is None:
        return max(device_folders, key=os.path.getmtime)

    # find folder with self.build_number in last 4 characters
    matching_folders = [f for f in device_folders if str(device.version.build) in f[len(device_folders[0]) - 4:]]
    if len(matching_folders) == 0:
        return None

    return max(matching_folders, key=os.path.getmtime)


def copy_local_file_to_remote(source_path_file, destination_path_file, host, user_name, password):
    """
    Method used to copy remote files from current location to remote
    Method will make an attempt to use file name specified in destination_path_file however if file name is not
    part of this path, then the source file name will be used. Destination path is not affected.
    :param source_path_file:
    :param destination_path_file:
    :param host:
    :param user_name:
    :param password:
    :return:
    """
    PrintMessage("Copy file: {0} to {1}:{2}".format(source_path_file, host, destination_path_file))
    destination_path = os.path.dirname(destination_path_file)

    with paramiko.SSHClient() as ssh:
        ssh.load_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user_name, password=password)

        with ssh.open_sftp() as sftp:
            try:
                sftp.chdir(destination_path)
            except IOError:
                sftp.mkdir(destination_path)
            finally:
                destination_file_name = os.path.basename(destination_path_file)
                if destination_file_name == '':
                    destination_file_name = os.path.basename(source_path_file)
                destination_file_with_path = destination_path + '/' + destination_file_name

                sftp.put(source_path_file, destination_file_with_path)

    return destination_file_with_path


def copy_file_to_remote_location_scp(cmd, file_path, source_machine):
    scp_command_temp = "scp -o StrictHostKeyChecking=no -o " \
                       "UserKnownHostsFile=/dev/null {0}@{1}:{2} ./."

    scp_command = scp_command_temp.format(source_machine['User'],
                                          source_machine['IP_Address'],
                                          file_path)
    cmd.send_cmd(scp_command, delay=3)
    cmd.cli.expect('password:')

    # After supplying password let pexpect wait until scp completed copying file i.e.
    # Value of 100% is found in: corero-defense-gx-V8.21.0.129_PGO.tar         100%   67MB   7.5MB/s   00:09
    cmd.send_cmd(source_machine['Password'], expected_value='100%')

    file_name = os.path.split(file_path)[1]
    is_remote_file_present_in_current_folder(cmd, file_name)

    return file_name


def copy_file_from_remote(host, user, src_file_path, dst_file_path):
    with paramiko.SSHClient() as ssh:
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, username=user.name, password=user.password)

        sftp_client = ssh.open_sftp()

        sftp_client.get(src_file_path, dst_file_path)
        sftp_client.close()

    return dst_file_path
