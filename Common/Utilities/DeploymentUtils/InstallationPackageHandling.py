#!/usr/bin/env python

from Common.Utilities.DeploymentUtils import DeploymentConstants
from Common.ConfigFiles.ConfigLoader import ConfigLoader


def get_ips_folder_path(device_version, prefix='', zero_fill=4):
    """
    Returns path to ips folder where packages are located
    :param device_version:
    :param prefix: GX has 'V' pefix in release and version folder names
    :param zero_fill: GX uses 3 digits to indicate build number
    :return:
    """
    release_folder = prefix + "{0}/"
    version_folder = prefix + "{1}/"
    package_path = release_folder + version_folder + "packages/"
    ips_path = ConfigLoader.get_test_run_config("Source_Values")["Package_Folder"] + package_path

    return ips_path.format(device_version.release_version, device_version.get_as_string(fill_with_zeros=zero_fill))


def get_vntd_package_path_ips(device_version, signed=True):
    if signed:
        package_name = DeploymentConstants.vNTD_PACKAGE_SIGNED_NAME.format(device_version.get_as_string())
    else:
        package_name = DeploymentConstants.vNTD_PACKAGE_NAME.format(device_version.get_as_string())

    source_path = get_ips_folder_path(device_version)
    return source_path + package_name


def get_intd_package_path_ips(device_version, signed=True, tar_file=False):
    if tar_file:
        package_name = DeploymentConstants.iNTD_TAR_PACKAGE_NAME.format(device_version.get_as_string())
    elif signed:
        package_name = DeploymentConstants.iNTD_PACKAGE_SINGED_NAME.format(device_version.get_as_string())
    else:
        package_name = DeploymentConstants.iNTD_PACKAGE_NAME.format(device_version.get_as_string())

    source_path = get_ips_folder_path(device_version)
    return source_path + package_name


def get_gx_ntd_package_path_ips(device_version, tar_file=False):
    """
    This covers:
    corero-defense-gx-V8.18.0.025_PGO.pkg
    corero-defense-gx-V8.18.0.025_PGO.tar

    :param tar_file:
    :param device_version:
    :return:
    """
    device_version_string = device_version.get_as_string(fill_with_zeros=3)
    if tar_file:
        package_name = DeploymentConstants.GX_NTD_TAR_PACKAGE_NAME.format(device_version_string)
    else:
        package_name = DeploymentConstants.GX_NTD_PACKAGE_NAME.format(device_version_string)

    source_path = get_ips_folder_path(device_version, prefix='V', zero_fill=3)
    return source_path + package_name


def get_cms_package_path_ips(device_version, signed=True, tar_file=False):
    if tar_file:
        package_name = DeploymentConstants.SMS_TAR_PACKAGE_NAME.format(device_version.get_as_string())
    elif signed:
        package_name = DeploymentConstants.SMS_PACKAGE_SIGNED_NAME.format(device_version.get_as_string())
    else:
        package_name = DeploymentConstants.SMS_PACKAGE_NAME.format(device_version.get_as_string())

    source_path = get_ips_folder_path(device_version)
    return source_path + package_name
