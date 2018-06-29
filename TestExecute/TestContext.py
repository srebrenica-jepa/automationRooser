#
# Bridge class between test runner and unittest
# It contains test environment information
#


class TestContext(object):
    current_config_file_name = None

    # holds information about currently deployed device build number
    build_number = None
    def_mode = None

    connection_details = None
    run_config = None

    deployed_devices = {}
    """ Contains list of devices, each device contains information:
    - device_type (ntd, cms, swa)
    - name
    - ip_address - device ip address
    - deployment_config (where applicable):
        - core count
        - network information (management, external, internal, secondary)"""

# global Test_Context
Test_Context = TestContext()
