#!/usr/bin/env python
# encoding: utf-8

# VMWARE Deployment
VM_DEVICE_NAME = "{0}_{1}_{2}"  # DeviceType_ReleaseName_autom i.e. NTD_CYGNUS_autom

Day0_NEW_SETTINGS = {
    "Subnet_Mask": "mgmt-subnet-mask: {0}\n",
    "Default_Gateway": "mgmt-default-gateway: {0}\n",
    "DNS_Domain": "dns-domain: {0}\n",
    "DNS_Servers": "dns-servers: {0}\n",
    "NTP_Servers": "ntp-servers: {0}\n"}

Day0_NEW_SETTING_HOSTNAME = "hostname: {0}\n"
Day0_NEW_SETTING_IP_ADDRESS = "mgmt-ipv4-address: {0}\n"

Day0_ISO_UPDATE_COMMANDS = [
    'mf() { sed -i "/$1/c$(openssl dgst -sha1 $1)" *.mf;}',
    'mkisofs -input-charset utf-8 -quiet -o day0cfg.iso day0cfg',
    'mf *.iso',
    'sed -i "/day0/s/\(size=\\"\)[^\\"]*/\\1$(stat -c%s *.iso)/" *.ovf',
    'mf *.ovf']

# {0} - device name
# {1} - hdd name (ESX)
# {2} - management nic
# {3} - data nic / external nic
# {4} - internal nic
# {5} - ova file
# {6} - full host address
# {7} - ESX server user name
# {8} - ESX server user password

OVF_COMMAND = "ovftool --overwrite --powerOffTarget --acceptAllEulas --name={0} --diskMode=thin --datastore={1} " \
              "{2} {3} {4} --powerOn {5} vi://{6}:{7}@{8}"

# Deployment
DEVICE_ALREADY_DEPLOYED = 'Device: {0} with build number {1} already deployed, skipping'

# Upgrade Packages (IPS Folder)- install, upgrade
vNTD_PACKAGE_NAME = 'corero-ntd-virtual-edition-vm-dpdk-{0}.pkg'
vNTD_PACKAGE_SIGNED_NAME = 'corero-ntd-virtual-edition-{0}.pkg'

iNTD_PACKAGE_NAME = 'corero-ntd1100-dpdk-{0}.pkg'
iNTD_PACKAGE_SINGED_NAME = 'corero-ntd1100-{0}.pkg'
iNTD_TAR_PACKAGE_NAME = 'corero-ntd-dpdk-{0}.tar'

iNTD_VERSION = 'ntd-({0}.0\d\d\d)'
iNTD_VERSION_RE = 'corero/ntd-(\d.\d.\d.\d+)'
iNTD_VERSION_RE_EXPECT = '(corero/ntd-\d.\d.\d.\d+)'

GX_NTD_PACKAGE_NAME = "corero-defense-gx-V{0}_PGO.pkg"
GX_NTD_TAR_PACKAGE_NAME = "corero-defense-gx-V{0}_PGO.tar"

SMS_PACKAGE_NAME = 'smartwall-cms-{0}.x86_64.pkg'
SMS_PACKAGE_SIGNED_NAME = 'smartwall-cms-{0}.x86_64-signed.pkg'
SMS_TAR_PACKAGE_NAME = 'smartwall-cms-{0}.x86_64.tar'
