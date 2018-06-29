#!/usr/bin/env python
import time
from re import search as re_search

from Common.Utilities.Logging import PrintMessage
from Common.Utilities.Enums import KVMDeviceState

# Deployment - KVM - virsh
VIRSH_DEVICE_SWITCHED_OFF = 'Domain {0} destroyed'
VIRSH_DEVICE_ALREADY_OFF = 'Requested operation is not valid: domain is not running'

# Device deployment - KVM - virsh
VIRSH_DEVICE_STATE = 'virsh domstate {0}'
VIRSH_TURN_OFF_DEVICE = 'virsh destroy {0}'
VIRSH_START_DEVICE = 'virsh start {0}'
VIRSH_GET_KVM_DEVICES = 'virsh domblklist {0}'


class VirshComm(object):
    def __init__(self, kvm_server):
        self.kvm_server = kvm_server
        self.kvm_prompt = kvm_server.user.name + '@'

    def send_virsh_cmd(self, command_line='', delay=1):
        self.kvm_server.send_cmd(command_line, expected_value=command_line, delay=delay)

        slept = 0
        while self.kvm_prompt not in self.kvm_server.cli.buffer:
            time.sleep(1)
            slept += 1
            if slept > 10:
                return []

        return self.kvm_server.cli.buffer.splitlines()

    @staticmethod
    def is_expected_message_in_virsh_response(expected_error, cli_buffer):
        buffer_list = cli_buffer.splitlines()
        for item in buffer_list:
            if expected_error in item:
                return True

        return False

    def turn_off_device(self, domain_name):
        """
        Method makes an attempt to turn off KVM device
        :param domain_name:
        :return:
        """
        PrintMessage('virsh - turn OFF device {0}'.format(domain_name))
        self.send_virsh_cmd(VIRSH_TURN_OFF_DEVICE.format(domain_name), delay=5)

        if self.is_expected_message_in_virsh_response(VIRSH_DEVICE_SWITCHED_OFF.format(domain_name),
                                                      self.kvm_server.cli.buffer):
            PrintMessage('virsh - device is switched off'.format(domain_name))
            return True
        elif self.is_expected_message_in_virsh_response(VIRSH_DEVICE_ALREADY_OFF,
                                                        self.kvm_server.cli.buffer):
            PrintMessage('virsh - device is already switched off'.format(domain_name))
            return True
        else:
            PrintMessage('virsh - failed to turn off device, error: \n {0}'.format(self.kvm_server.cli.before))
            return False

    def turn_on_device(self, domain_name):
        """
        Switches on device
        :param domain_name:
        :return:
        """
        PrintMessage('virsh - turn ON device {0}'.format(domain_name))
        if 'ntd' in domain_name.lower():
            delay = 180
        else:
            delay = 60
        self.send_virsh_cmd(VIRSH_START_DEVICE.format(domain_name), delay=delay)

    def get_domain_state(self, domain_name):
        """
        Method uses virsh to check if deployed device is expected

        :param domain_name: domain name set in virsh, device name
        :return: Returns a string from defined enum: either not_found, offline, online
        """
        self.send_virsh_cmd(VIRSH_DEVICE_STATE.format(domain_name))
        cli_buffer = self.kvm_server.cli.buffer

        if self.is_expected_message_in_virsh_response('Domain not found', cli_buffer):
            return KVMDeviceState.not_found
        elif self.is_expected_message_in_virsh_response('shut off', cli_buffer):
            return KVMDeviceState.offline
        elif self.is_expected_message_in_virsh_response('running', cli_buffer):
            return KVMDeviceState.online
        else:
            raise Exception('get_domain_state: unknown state: {0}'.format(self.kvm_server.cli.buffer))

    def get_disk_paths(self, domain_name):
        re_exp = ".*\s(.*\/[^\/]*)$"
        command_line_output = self.send_virsh_cmd(VIRSH_GET_KVM_DEVICES.format(domain_name), delay=2)

        disks_path = []
        for line_item in command_line_output:
            if '.qcow2' in line_item:
                re_search_result = re_search(re_exp, line_item)
                disks_path.append(re_search_result.group(1))

        return disks_path
