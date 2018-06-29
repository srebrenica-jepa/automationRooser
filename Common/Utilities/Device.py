#!/usr/bin/env python
from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.Utilities.Enums import DeviceType
from Common.Utilities.Version import Version


class DeviceManager(object):
    @staticmethod
    def get_device_type_from_name(device_name):
        """
        Assumes names are either swa, cms, ntd0, ntd1
        :param device_name:
        :return: swa, cms or ntd
        """
        all_types = [getattr(DeviceType, i) for i in dir(DeviceType) if not i.startswith('__')]

        for device_type in all_types:
            if device_type in device_name.lower():
                return device_type

        raise Exception('invalid device name :{0}, name is expected to include its type i.e.: {1}'.format(device_name,
                                                                                                          all_types))

    @staticmethod
    def create_device_template_from_config(device_name):
        deployment_values = ConfigLoader.get_test_run_config('Deployment_Values')

        device = Device(device_name,
                        DeviceManager.get_device_type_from_name(device_name),
                        deployment_values[device_name]['IP_ADDRESS'],
                        deployment_values[device_name]['Deployment_Type'],
                        deployment_values[device_name]['Device_Release'])

        for key in deployment_values[device_name].keys():
            if key in ['IP_ADDRESS', 'Deployment_Type', 'Device_Release']:
                continue

            device.deployment_config[key] = deployment_values[device_name][key]

        return device


class Device(object):
    """
    Object describing an device (ntd, cms, swa)
    variable version is used to indicate its current build of deployed device or
    intended version of during the deployment process
    """
    def __init__(self, name, device_type, ip_address, deployment_type, device_release):
        """

        :param name: deice name
        :param device_type:
        :param ip_address: device ip address
        :param deployment_type: class DeploymentType(object):
            kvm = 'kvm'
            vmware = 'vmware'
            ntd1100 = 'ntd1100'
            gx = 'gx'
        :param device_release:
        """
        self._name = name
        self._device_type = device_type
        self._ip_address = ip_address
        self._version = None
        self._deployment_type = deployment_type

        self.version = device_release

        # stores network interface names, used for deployment
        self.deployment_config = {}

    @property
    def name(self):
        """
        Name by which device is known to CMS.
        :return:
        """
        return self._name

    @property
    def device_type(self):
        """
        Either cms, ntd or swa
        :return:
        """
        return self._device_type

    @property
    def ip_address(self):
        """
        Host address
        :return:
        """
        return self._ip_address

    @property
    def version(self):
        """
        Version object describing deployed device or device to be deployed
        :return:
        """
        return self._version

    @property
    def deployment_type(self):
        """
        Either ntd1100, kvm, vm or gx or any other (future proof! yay!)
        :return:
        """
        return self._deployment_type

    @version.setter
    def version(self, value):
        self._version = Version(value)
