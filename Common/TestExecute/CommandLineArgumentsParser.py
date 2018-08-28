#!/usr/bin/env python
import argparse
import os

import Common.Utilities.Enums
from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.Utilities.Device import DeviceManager
from Common.Utilities.Logging import PrintMessage
from TestExecute.TestContext import Test_Context

# Parse Argument messages
BUILD_NUMBER_TEST_MESSAGE = 'Required build number to upload test results.'
BUILD_NUMBER_DEPLOY_MESSAGE = 'Optional argument to specify build number.'
DEF_MODE_MESSAGE = 'Defense mode, defaults to mitigate.'
CORES_MESSAGE = 'Specifies NTD core count, defaults to 2-core.'
DO_NOT_DISABLE_ALL_RULES = 'Option to DO NOT disable all rules prior executing test.'
DEBUG_MESSAGE = 'Special option to set debug flag, this is used to various ends in test code'
DEVICE_TYPE_MESSAGE = 'Specifies device name(s) to deploy. Same device name as in selected configuration file.'
HOST_ADDRESS = 'Host name, IP Address'
REPORT_RECIPIENTS_MESSAGE = 'String parameter listing email recipients, comma delimited'
POST_DEPLOY_WAIT_TIME_MESSAGE = 'Wait time for after deployment to let the devices settle down, default is 1800 secs'
DEPLOY_DEVICES_MESSAGE = 'If selected framework will deploy devices required to perform test run (CMS and NTD(s))'
CONFIGURE_ALL = 'Perform whole test configuration CMS and client/server'
LOOP_COUNT_MESSAGE = 'Amount of times selected tests will be executed, default value is 1'
LUF_COUNT_MESSAGE = 'Keep executing test suite until its first failure. If loop is left unused, max loop count ' \
                    'is set to 50.'
RE_RUN_MESSAGE = 'Re-runs failed tests'
LOG_DROP_FOLDER_MESSAGE = 'Full path to test drop location. Test log and diagnostics will be dropped there.' \
                          'Folder location will be included in test report.'
TEST_IDS = 'Specify single test rail ID'
TEST_CLASS_NAME = 'Specify name of the test class, partial name is sufficient. Tests from all matched classes ' \
                  'will be executed.'
TestClassNameOrTestCaseID = 'Required either test class name(s) or test case ID(s).'
RUN_CONFIG_SELECTION = 'Configuration file used during test execution.'
TEST_CONTEST_INFO = 'TestContext configuration: {0}'


def update_test_context_with_device_details(current_config_file_name):
    """
    This method needs to be run before executing tests or any other methods that are config dependant
    :param current_config_file_name:
    :return:
    """
    Test_Context.current_config_file_name = './ConfigFiles/TestRunConfig_{0}.json'.format(current_config_file_name)
    Test_Context.run_config = ConfigLoader.get_test_run_config()

    Test_Context.def_mode = Test_Context.run_config.load('TestPremise')['DefMode']
    Test_Context.connection_details = ConfigLoader.get_general_config('DeviceConnectionDetails')
    deployment_values = Test_Context.run_config.load('Deployment_Values')

    for device_name in deployment_values.keys():
        Test_Context.deployed_devices[device_name] = DeviceManager.create_device_template_from_config(device_name)


class CommandLineArgumentsParser(object):
    @staticmethod
    def get_available_config_files(prefix, postfix):
        """
        Configuration files are expected to be in format TestRunConfig_XYZ.json
        The TestRunConfig_ and .json are stripped off.
        :param prefix:
        :param postfix:
        :return:
        """
        available_config_fields = []

        for config_file in os.listdir('./ConfigFiles'):
            if config_file.startswith(prefix) and config_file.endswith(postfix):

                # 14:-5 remove TestRunConfig_ and .json
                available_config_fields.append(config_file[14:-5])

        return available_config_fields

    @staticmethod
    def read_default_config():
        default_config = None
        try:
            with open('./ConfigFiles/default_config') as f:
                default_config = f.readline()

        except IOError:
            default_config = None
        finally:
            return default_config

    @staticmethod
    def add_argument_configuration_file(parser):
        config_files = CommandLineArgumentsParser.get_available_config_files('TestRunConfig_', '.json')
        default_config = CommandLineArgumentsParser.read_default_config()

        parser.add_argument('-c',
                            dest='config_file',
                            help=RUN_CONFIG_SELECTION,
                            choices=config_files,
                            default=default_config,
                            required=True)

    @staticmethod
    def add_argument_configuration_all(parser):
        parser.add_argument('--all',
                            dest='all_configuration',
                            help=CONFIGURE_ALL,
                            default=False,
                            action='store_true')

    @staticmethod
    def add_argument_build_number(parser):
        parser.add_argument("-b",
                            dest='build',
                            help=BUILD_NUMBER_DEPLOY_MESSAGE,
                            type=int,
                            default=None)

    @staticmethod
    def add_argument_host_address(parser):
        parser.add_argument('-H',
                            dest='host_address',
                            required=True,
                            help=HOST_ADDRESS)

    @staticmethod
    def add_argument_list_of_report_recipients(parser):
        parser.add_argument('-r',
                            nargs='*',
                            dest='report_recipients',
                            help=REPORT_RECIPIENTS_MESSAGE,
                            default=[])

    @staticmethod
    def add_argument_post_deploy_wait_time(parser):
        parser.add_argument('-w',
                            dest='post_deploy_wait_time',
                            help=POST_DEPLOY_WAIT_TIME_MESSAGE,
                            type=int,
                            default=1800)

    @staticmethod
    def add_argument_deploy_devices(parser):
        parser.add_argument('--do_deploy',
                            dest='do_deploy',
                            help=DEPLOY_DEVICES_MESSAGE,
                            default=False,
                            action='store_true')

    @staticmethod
    def add_argument_list_of_test_ids(parser):
        parser.add_argument('-t',
                            nargs='*',
                            dest='test_ids',
                            type=int,
                            help=TEST_IDS,
                            default=[])

    @staticmethod
    def add_argument_list_of_class_names(parser):
        parser.add_argument('-class',
                            nargs='*',
                            dest='test_class_names',
                            type=str,
                            help=TEST_CLASS_NAME,
                            default=[])

    @staticmethod
    def add_argument_execute_in_loop(parser):
        parser.add_argument('-l',
                            dest='loop_count',
                            help=LOOP_COUNT_MESSAGE,
                            type=int,
                            default=1)

    @staticmethod
    def add_argument_execute_in_loop_until_failure(parser):
        parser.add_argument('--luf',
                            dest='loop_until_failure',
                            help=LUF_COUNT_MESSAGE,
                            default=False,
                            action='store_true')

    @staticmethod
    def add_argument_re_run_failed(parser):
        parser.add_argument('--rerun',
                            dest='rerun',
                            help=RE_RUN_MESSAGE,
                            default=False,
                            action='store_true')

    @staticmethod
    def add_argument_log_file_path(parser):
        """
        Passed in argument is full path with file name to test log file
        Log path will be used to drop diagnostic files after test run.
        :param parser:
        :return:
        """
        parser.add_argument('-log_drop_folder',
                            dest='log_drop_folder',
                            help=LOG_DROP_FOLDER_MESSAGE,
                            action='store')

    @staticmethod
    def add_argument_def_mode(parser):
        parser_choices = [Common.Utilities.Enums.DefenseMode.mitigate, Common.Utilities.Enums.DefenseMode.monitor]
        parser.add_argument("-d",
                            dest='def_mode',
                            help=DEF_MODE_MESSAGE,
                            default=Common.Utilities.Enums.DefenseMode.mitigate,
                            required=False,
                            choices=parser_choices)

    @staticmethod
    def add_argument_do_not_disable_all_rules(parser):
        parser.add_argument("--do_not_disable_all_rules",
                            dest='do_not_disable_all_rules',
                            default=False,
                            help=DO_NOT_DISABLE_ALL_RULES,
                            action='store_true')

    @staticmethod
    def add_argument_device_selection(parser):
        parser.add_argument('-d',
                            default=[],
                            nargs='*',
                            dest='devices',
                            required=True,
                            help=DEVICE_TYPE_MESSAGE)

    # used in ESX deployment
    @staticmethod
    def process_arguments_deployment():
        parser = argparse.ArgumentParser(prefix_chars='-')
        CommandLineArgumentsParser.add_argument_configuration_file(parser)

        CommandLineArgumentsParser.add_argument_device_selection(parser)
        CommandLineArgumentsParser.add_argument_build_number(parser)

        parsed_args = parser.parse_args()
        update_test_context_with_device_details(parsed_args.config_file)

        return parsed_args

    #
    # it would make sense to add the def mode as well, however tests would have to be updated
    # to work with scenario where block rules are not really blocking
    # - core number does not really affect tests atm
    #

    @staticmethod
    def process_arguments_single_test_run():
        """
        Command line test run with specified set of tests either by class or test ids
        :return:
        """
        parser = argparse.ArgumentParser(prefix_chars='-')
        CommandLineArgumentsParser.add_argument_do_not_disable_all_rules(parser)
        CommandLineArgumentsParser.add_argument_def_mode(parser)
        CommandLineArgumentsParser.add_argument_configuration_file(parser)
        CommandLineArgumentsParser.add_argument_list_of_test_ids(parser)
        CommandLineArgumentsParser.add_argument_list_of_class_names(parser)
        CommandLineArgumentsParser.add_argument_execute_in_loop(parser)
        CommandLineArgumentsParser.add_argument_execute_in_loop_until_failure(parser)

        # test
        CommandLineArgumentsParser.add_argument_build_number(parser)
        CommandLineArgumentsParser.add_argument_list_of_report_recipients(parser)

        parsed_args = parser.parse_args()

        Test_Context.do_not_disable_all_rules = parsed_args.do_not_disable_all_rules
        Test_Context.def_mode = parsed_args.def_mode

        PrintMessage(TEST_CONTEST_INFO.format(vars(Test_Context)))

        if len(parsed_args.test_ids) == 0 and len(parsed_args.test_class_names) == 0:
            parser.error(TestClassNameOrTestCaseID)

        update_test_context_with_device_details(parsed_args.config_file)

        return parsed_args

    # used by the RunAll, RunRegression, RunSmoke
    @staticmethod
    def process_arguments_group_test_run():
        """
        RunAll, RunSmoke, RunRegression type of runs
        :return:
        """
        parser = argparse.ArgumentParser(prefix_chars='-')
        CommandLineArgumentsParser.add_argument_build_number(parser)
        CommandLineArgumentsParser.add_argument_do_not_disable_all_rules(parser)
        CommandLineArgumentsParser.add_argument_def_mode(parser)
        CommandLineArgumentsParser.add_argument_configuration_file(parser)
        CommandLineArgumentsParser.add_argument_list_of_report_recipients(parser)
        CommandLineArgumentsParser.add_argument_post_deploy_wait_time(parser)
        CommandLineArgumentsParser.add_argument_deploy_devices(parser)
        CommandLineArgumentsParser.add_argument_re_run_failed(parser)
        CommandLineArgumentsParser.add_argument_log_file_path(parser)

        parsed_args = parser.parse_args()

        Test_Context.do_not_disable_all_rules = parsed_args.do_not_disable_all_rules
        Test_Context.log_drop_folder = parsed_args.log_drop_folder

        PrintMessage(TEST_CONTEST_INFO.format(vars(Test_Context)))
        update_test_context_with_device_details(parsed_args.config_file)
        return parsed_args

    # executing the test bed configuration
    @staticmethod
    def process_arguments_simple_setup_no_run():
        parser = argparse.ArgumentParser(prefix_chars='-')
        CommandLineArgumentsParser.add_argument_configuration_file(parser)
        CommandLineArgumentsParser.add_argument_configuration_all(parser)

        parsed_args = parser.parse_args()

        update_test_context_with_device_details(parsed_args.config_file)

        return parsed_args

    @staticmethod
    def process_arguments_support_login():
        parser = argparse.ArgumentParser(prefix_chars='-')
        CommandLineArgumentsParser.add_argument_host_address(parser)

        parsed_args = parser.parse_args()

        Test_Context.connection_details = ConfigLoader.get_general_config('DeviceConnectionDetails')

        return parsed_args
