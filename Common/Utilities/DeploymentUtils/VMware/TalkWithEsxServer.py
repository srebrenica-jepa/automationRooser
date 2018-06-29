#!/usr/bin/env python

# Copyright 2016 use of pyVim library
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import atexit
import ssl
import sys
import time

import requests
from pyVim import connect
from pyVmomi import vim

from Common.Utilities.Libs.retry.api import retry
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.TestExceptions import VMNotFound
from Common.ConfigFiles.ConfigLoader import ConfigLoader

requests.packages.urllib3.disable_warnings()


class TalkWithESX(object):
    @staticmethod
    def get_connector():
        """
        sys.version_info returns python version (major, minor, build)
        we do not want SSL context to be used with python where build is less than 13
        :return:
        """
        run_config = ConfigLoader.get_test_run_config('VMWare_Values')

        if sys.version_info[0] == 2 and sys.version_info[2] < 13:
            esx_connection = connect.SmartConnect(host=run_config['Host'],
                                                  user=run_config['ESX_User'],
                                                  pwd=run_config['ESX_Password'])
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            esx_connection = connect.SmartConnect(host=run_config['Host'],
                                                  user=run_config['ESX_User'],
                                                  pwd=run_config['ESX_Password'],
                                                  sslContext=context)

        atexit.register(connect.Disconnect, esx_connection)
        return esx_connection

    @staticmethod
    def _get_nic_template(device_name, operation):
        switch_spec = vim.vm.device.VirtualDeviceSpec()
        switch_spec.operation = operation

        switch_spec.device = vim.vm.device.VirtualVmxnet3()
        switch_spec.device.backing = vim.vm.device.VirtualEthernetCard.NetworkBackingInfo()
        switch_spec.device.backing.deviceName = device_name

        if operation == vim.vm.device.VirtualDeviceSpec.Operation.remove:
            return switch_spec

        switch_spec.device.connectable = vim.vm.device.VirtualDevice.ConnectInfo()
        switch_spec.device.connectable.startConnected = True
        switch_spec.device.connectable.connected = True

        return switch_spec

    @staticmethod
    @retry(exceptions=VMNotFound, delay=10, tries=6)
    def _find_vm_by_name(vm_name):
        """
        Method used to find the Virtual Machine by its name
        If Virtual Machine is not found an exception is raised.
        :param vm_name: name of the Virtual Machine
        :return: returns managed object reference (if found)
        """

        connector = TalkWithESX.get_connector()
        vm_found = connector.content.searchIndex.FindByDnsName(None, vm_name, True)

        if vm_found:
            return vm_found

        raise VMNotFound('VM machine not found for given vm name: {0}'.format(vm_name))

    @staticmethod
    @retry(exceptions=VMNotFound, delay=10, tries=6)
    def _find_vm_by_ip(vm_ip, check_once=False):
        """
        Method used to find the Virtual Machine by its ip address
        If Virtual Machine is not found an exception is raised.
        :param vm_ip: ip address of the Virtual Machine
        :return: managed object reference to found machine (if found)
        """

        connector = TalkWithESX.get_connector()
        vm_found = connector.content.searchIndex.FindByIp(None, vm_ip, True)

        if vm_found:
            return vm_found
        elif check_once:
            return None

        raise VMNotFound('VM machine not found for given ip address: {0}'.format(vm_ip))

    @staticmethod
    def _wait_for_task(task, message):
        """
        Common method used wait for given task to finish, it periodically checks the task state
        :param task: vm_task describing job given to vSphere
        :return: None
        """

        PrintMessage('TalkWithEsxServer > Waiting for VM task: {0} to finish'.format(message))
        while task.info.state == 'running':
            time.sleep(1)

        time.sleep(1)
        message = 'TalkWithEsxServer > state: {0} '.format(task.info.state)
        if task.info.error:
            message += str(task.info.error)

        PrintMessage(message)

    @staticmethod
    def switch_off_vm(vm_ip):
        """
        Static method used to turn of VM Machine
        :param vm_ip: address of the Virtual Machine (VM)
        :return: None
        """

        vm = TalkWithESX._find_vm_by_ip(vm_ip, check_once=True)

        if vm is None:
            return

        PrintMessage("TalkWithEsxServer >> Found: {0}".format(vm.name))
        PrintMessage("TalkWithEsxServer >> The current powerState is: {0}".format(vm.runtime.powerState))

        if format(vm.runtime.powerState) == "poweredOn":
            PrintMessage("TalkWithEsxServer >> Attempting to power off {0}".format(vm.name))
            vm_task = vm.PowerOffVM_Task()
            TalkWithESX._wait_for_task(vm_task, 'switch vm off')

        return vm

    @staticmethod
    def _delete_vm(vm_ip):
        """
        Static method used to delete VM Machine from vSphere
        :param vm_ip: address of the Virtual Machine (VM)
        :return: None
        """

        vm = TalkWithESX.switch_off_vm(vm_ip)
        vm_task = vm.Destroy_Task()
        TalkWithESX._wait_for_task(vm_task, 'delete vm')

    @staticmethod
    def _edit_configuration(vm, device):
        """
        :param vm: VM machine handler, managed object reference
        :param device: the descriptor containing new updated configuration
        :return: None
        """

        spec = vim.vm.ConfigSpec()

        # add Switch here
        dev_changes = []
        switch_spec = vim.vm.device.VirtualDeviceSpec()
        switch_spec.operation = vim.vm.device.VirtualDeviceSpec.Operation.edit
        switch_spec.device = device
        dev_changes.append(switch_spec)

        spec.deviceChange = dev_changes
        vm_task = vm.ReconfigVM_Task(spec=spec)
        TalkWithESX._wait_for_task(vm_task, 'edit vm conf')

    @staticmethod
    def find_network_device(vm_devices, device_name, return_device=0):
        e1000 = vim.vm.device.VirtualE1000
        vmxnet3 = vim.vm.device.VirtualVmxnet3

        found_devices = [i for i in vm_devices if type(i) in [e1000, vmxnet3] and i.backing.deviceName == device_name]

        if len(found_devices) == 0:
            return None

        return found_devices[return_device]

    @staticmethod  # - work in progress
    def toggle_network_connection_on_vm(vm_ip, device_name, state):
        """
        Static method used to find VM Machine and toggle state of its network device

        :param vm_ip: ip address of targeted VM machine
        :param device_name: the interface name NIC is associated with (also used as id)
        :param state: False / True to indicate desired state
        :return: None
        """

        managed_object_reference = TalkWithESX._find_vm_by_ip(vm_ip)

        # name = 'rderinger-internal-vSwitch'
        found_device = TalkWithESX.find_network_device(managed_object_reference.config.hardware.device,
                                                       device_name)
        if found_device is None:
            message = "Device '{0}' not found on the VM machine with ip address {1}"
            raise Exception(message.format(device_name, vm_ip))

        found_device.connectable.connected = state

        message = 'TalkWithEsxServer > connection state device {0}:{1} and state: {2}'.format(device_name,
                                                                                              vm_ip,
                                                                                              state)
        PrintMessage(message)
        TalkWithESX._edit_configuration(managed_object_reference, found_device)

    @staticmethod
    def add_pair_port(vm_ip, external, internal):
        """
        method to add new nic to an esx device

        vim.vm.device.VirtualDeviceSpec.Operation.add
        vim.vm.device.VirtualDeviceSpec.Operation.remove
        :param vm_ip: esx machine
        :param external: name of a new nic
        :param internal: name of a new nic
        :return:
        """

        managed_object_reference = TalkWithESX._find_vm_by_ip(vm_ip)

        found_device1 = TalkWithESX.find_network_device(managed_object_reference.config.hardware.device,
                                                        external)

        found_device2 = TalkWithESX.find_network_device(managed_object_reference.config.hardware.device,
                                                        internal)

        operation = vim.vm.device.VirtualDeviceSpec.Operation.add
        spec = vim.vm.ConfigSpec()

        # if port pair exists
        if found_device1 is None:
            spec.deviceChange.append(TalkWithESX._get_nic_template(external, operation))
        if found_device2 is None:
            spec.deviceChange.append(TalkWithESX._get_nic_template(internal, operation))

        if len(spec.deviceChange) == 0:
            return

        vm_task = managed_object_reference.PowerOffVM_Task()
        TalkWithESX._wait_for_task(vm_task, 'switch off')

        vm_task = managed_object_reference.ReconfigVM_Task(spec=spec)
        TalkWithESX._wait_for_task(vm_task, 'reconfigure vm')

        # power up and wait until it's up
        vm_task = managed_object_reference.PowerOnVM_Task()
        TalkWithESX._wait_for_task(vm_task, 'switch on')
        TalkWithESX._find_vm_by_ip(vm_ip)

    @staticmethod
    def remove_pair_port(vm_ip, external, internal):
        """
        method to add new nic to an esx device

        vim.vm.device.VirtualDeviceSpec.Operation.add
        vim.vm.device.VirtualDeviceSpec.Operation.remove
        :param vm_ip: esx machine
        :param external: name of a new nic
        :param internal: name of a new nic
        :return:
        """

        managed_object_reference = TalkWithESX._find_vm_by_ip(vm_ip)

        found_device1 = TalkWithESX.find_network_device(managed_object_reference.config.hardware.device,
                                                        external)

        found_device2 = TalkWithESX.find_network_device(managed_object_reference.config.hardware.device,
                                                        internal)

        spec = vim.vm.ConfigSpec()
        # if port pair exists
        if found_device1 is not None:
            device_change = vim.vm.device.VirtualDeviceSpec()
            device_change.device = found_device1
            device_change.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
            spec.deviceChange.append(device_change)

        if found_device2 is not None:
            device_change = vim.vm.device.VirtualDeviceSpec()
            device_change.device = found_device2
            device_change.operation = vim.vm.device.VirtualDeviceSpec.Operation.remove
            spec.deviceChange.append(device_change)

        if len(spec.deviceChange) == 0:
            return

        vm_task = managed_object_reference.PowerOffVM_Task()
        TalkWithESX._wait_for_task(vm_task, 'switch off')

        vm_task = managed_object_reference.ReconfigVM_Task(spec=spec)
        TalkWithESX._wait_for_task(vm_task, 'reconfigure vm')

        # power up and wait until it's up
        vm_task = managed_object_reference.PowerOnVM_Task()
        TalkWithESX._wait_for_task(vm_task, 'switch on')
        TalkWithESX._find_vm_by_ip(vm_ip)
