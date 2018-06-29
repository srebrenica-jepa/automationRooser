#!/usr/bin/env python
from ..Utilities.JsonReader import JsonReader
from TestExecute.TestContext import Test_Context


class ConfigLoader(object):
    @classmethod
    def get_test_run_config(cls, load_section=None):
        return cls._load_config(Test_Context.current_config_file_name, load_section)

    @classmethod
    def _load_config(cls, file_path, load_section=None):
        config_file = JsonReader(file_path)

        if load_section is not None:
            return config_file.load(load_section)
        else:
            return config_file

    @classmethod
    def get_general_config(cls, section):
        """
        General config contains FTP details and Connection details i.e. port values
        :param section:
        :return:
        """
        return cls._load_config("./Common/ConfigFiles/GeneralConfig.json", section)

    @classmethod
    def get_test_report_config(cls):
        return cls._load_config("./Common/TestReporting/TestReportConfig.json", 'TestRailConnection')

    @classmethod
    def get_deployment_config(cls, load_section=None):
        return cls._load_config("./Common/Utilities/DeploymentUtils/DeploymentConfig.json", load_section)
