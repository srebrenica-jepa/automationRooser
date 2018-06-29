#!/usr/bin/env python

from Common.TestExecute.TestRunner import TestRunner
from Common.Utilities import Enums
from Common.Utilities.Logging import PrintMessage
from TestExecute.CommandLineArgumentsParser import CommandLineArgumentsParser
from TestExecute.TestContext import Test_Context


class RunManager(object):
    def __init__(self):
        self.test_runner = TestRunner()

    def _run_smoke(self, build_number):
        test_run_id = Test_Context.run_config.load('TestRun_Detail')['Smoke_Run_Id']
        self.test_runner.execute_test_suite('SmokeSuite', build_number, test_run_id)

    def _run_regression(self, build_number):
        test_run_id = Test_Context.run_config.load('TestRun_Detail')['Regression_Run_Id']
        self.test_runner.execute_test_suite('RegressionSuite', build_number, test_run_id)

    def _run_all(self, build_number, report_recipients):
        regression_test_run_id = Test_Context.run_config.load('TestRun_Detail')['Regression_Run_Id']
        smoke_test_run_id = Test_Context.run_config.load('TestRun_Detail')['Smoke_Run_Id']

        time_taken = self.test_runner.execute_test_suite('SmokeSuite', build_number, smoke_test_run_id)
        time_taken += self.test_runner.execute_test_suite('RegressionSuite', build_number, regression_test_run_id)

        # currently regression and smoke suites are housed in the same test run
        # might need to change it once those two are split in UIAutomation
        self.test_runner.send_report(regression_test_run_id, report_recipients, time_taken)

    def run_bunch(self):
        parsed_args = CommandLineArgumentsParser.process_arguments_group_test_run()

        if parsed_args.run_type == Enums.RunTypes.AllTests:
            self._run_all(parsed_args.build, parsed_args.report_recipients)
            PrintMessage('<<<<<<<<<<<<<<<<Test run - ALL complete!>>>>>>>>>>>>>>>>')

        elif parsed_args.run_type == Enums.RunTypes.Smoke:
            self._run_smoke(parsed_args.build)
            PrintMessage('<<<<<<<<<<<<<<<<Test run - Smoke complete!>>>>>>>>>>>>>>>>')

        elif parsed_args.run_type == Enums.RunTypes.Regression:
            self._run_regression(parsed_args.build)
            PrintMessage('<<<<<<<<<<<<<<<<Test run - Regression complete!>>>>>>>>>>>>>>>>')