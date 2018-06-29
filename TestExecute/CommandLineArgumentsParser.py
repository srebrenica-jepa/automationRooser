#!/usr/bin/env python
import argparse

import os

from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.Utilities import Enums
from TestExecute.TestContext import Test_Context

# Parse Argument messages
BUILD_NUMBER_DEPLOY_MESSAGE = 'Optional argument to specify build number.'
RUN_TYPE_MESSAGE = 'Specify run type'
HOST_ADDRESS = 'Host name, IP Address'
REPORT_RECIPIENTS_MESSAGE = 'String parameter listing email recipients, comma delimited'
TEST_IDS = 'Specify single test rail ID'
TEST_CLASS_NAME = 'Specify name of the test class, partial name is sufficient. Tests from all matched classes ' \
                  'will be executed.'
TestClassNameOrTestCaseID = 'Required either test class name(s) or test case ID(s).'
RUN_CONFIG_SELECTION = 'Configuration file used during test execution.'


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
    def add_argument_build_number(parser):
        parser.add_argument("-b",
                            dest='build',
                            help=BUILD_NUMBER_DEPLOY_MESSAGE,
                            type=int,
                            default=None)

    @staticmethod
    def add_argument_run_type(parser):
        parser.add_argument("-run_type",
                            dest='run_type',
                            help=RUN_TYPE_MESSAGE,
                            required=True,
                            choices=Enums.list_enum(Enums.RunTypes))

    @staticmethod
    def add_argument_list_of_report_recipients(parser):
        parser.add_argument('-r',
                            nargs='*',
                            dest='report_recipients',
                            help=REPORT_RECIPIENTS_MESSAGE,
                            default=[])

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

    #
    # it would make sense to add the def mode as well, however tests would have to be updated
    # to work with scenario where block rules are not really blocking
    # - core number does not really affect tests atm
    #

    @staticmethod
    def process_arguments_single_test_run():
        parser = argparse.ArgumentParser(prefix_chars='-')
        CommandLineArgumentsParser.add_argument_configuration_file(parser)
        CommandLineArgumentsParser.add_argument_list_of_test_ids(parser)
        CommandLineArgumentsParser.add_argument_list_of_class_names(parser)

        parsed_args = parser.parse_args()

        if len(parsed_args.test_ids) == 0 and len(parsed_args.test_class_names) == 0:
            parser.error(TestClassNameOrTestCaseID)

        Test_Context.current_config_file_name = './ConfigFiles/TestRunConfig_{0}.json'.format(parsed_args.config_file)
        Test_Context.run_config = ConfigLoader.get_test_run_config()

        return parsed_args.test_ids, parsed_args.test_class_names

    # used by the RunAll, RunRegression, RunSmoke
    @staticmethod
    def process_arguments_group_test_run():
        parser = argparse.ArgumentParser(prefix_chars='-')
        CommandLineArgumentsParser.add_argument_configuration_file(parser)
        CommandLineArgumentsParser.add_argument_build_number(parser)
        CommandLineArgumentsParser.add_argument_list_of_report_recipients(parser)
        CommandLineArgumentsParser.add_argument_run_type(parser)

        parsed_args = parser.parse_args()

        Test_Context.current_config_file_name = './ConfigFiles/TestRunConfig_{0}.json'.format(parsed_args.config_file)
        Test_Context.run_config = ConfigLoader.get_test_run_config()

        return parsed_args
