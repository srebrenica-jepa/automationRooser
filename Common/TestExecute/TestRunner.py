#!/usr/bin/env python
import imp
import inspect
import os
import sys
import time
import traceback
import unittest

from Common.TestExecute import TestFuncs
from Common.TestReporting import TestRailUploader
from Common.TestReporting.ReportGenerator import ReportGenerator
from Common.Utilities.Logging import PrintMessage
from Common.Utilities.Logging import StreamToLogger


class TestRunner(unittest.TextTestRunner):
    def __init__(self, log_drop_folder=None, config_name=None):
        """

        :param log_drop_folder: test log location, can be None
        """
        super(TestRunner, self).__init__(stream=StreamToLogger(log_drop_folder, config_name))

        self.re_run_failed = False
        self.rebuild_configuration_callback = None

    def re_run_failed_tests(self, results):
        """
        Method will retrieve list of failed and errored tests
        Method will re-run those failed tests
        Method will update results by removing tests from failed/errored if test is a pass in the re-run
        :param results:
        :return:
        """
        if self.rebuild_configuration_callback:
            self.rebuild_configuration_callback(all_configuration=False)

        PrintMessage("-----===== ################################ =====-----")
        PrintMessage("-----===== Re-RUNNING failed tests STARTED. =====-----")
        PrintMessage("-----===== ################################ =====-----")

        failed_test_ids = TestFuncs.get_re_run_test_ids(results)
        PrintMessage("Test IDs to re-run : {0}".format(failed_test_ids))

        re_run_suite = self.get_suite_from_test_ids(failed_test_ids)
        re_run_result = self.run(re_run_suite)
        TestFuncs.ResultUpdater.update_results_with_re_run(results, re_run_result)

        PrintMessage("-----===== ############################## =====-----")
        PrintMessage("-----===== Re-RUNNING failed tests ENDED. =====-----")
        PrintMessage("-----===== ############################## =====-----")

    def run_test(self, test_suite):
        start_time = time.time()

        try:
            results = self.run(test_suite)

            less_than_10_percent_failed = len(results.failures + results.errors) < float(len(test_suite._tests))/10
            if self.re_run_failed and less_than_10_percent_failed:
                self.re_run_failed_tests(results)

        finally:
            stop_time = time.time()
            time_taken = stop_time - start_time

        return results, time_taken

    @staticmethod
    def upload_results(test_results, all_tests, build_number, test_run_id):
        try:
            if build_number:
                result_uploader = TestRailUploader.TestRailResultUploader(test_run_id, build_number)
                result_uploader.process_and_upload(test_results, all_tests)
        except Exception as e:
            tb = traceback.format_exc()
            PrintMessage('_upload_results > Encountered exception {0}, with args {1}'.format(type(e), e.args))
            PrintMessage(str(e))
            PrintMessage("_upload_results > traceback: {0}".format(tb))
            pass

    @staticmethod
    def _get_list_of_test_files(test_files_path, test_type):
        """
        the type is used to get correct files (either RegressionSuite or SmokeSuite)
        :param test_files_path:
        :param test_type:
        :return:
        """
        def filter_fun(x): return 'pyc' not in x and '__init__' not in x and '.orig' not in x and test_type in x
        tests_files = os.listdir(test_files_path)
        return filter(filter_fun, tests_files)

    # returns list of classes
    # the type is used to get correct files (either RegressionSuite or SmokeSuite)
    # returns list of pairs: 'name_of_class', actual class; the latter is used in test execution

    def get_test_classes(self, with_file_name):
        test_files_path = os.getcwd() + '/Tests'

        test_files = self._get_list_of_test_files(test_files_path, with_file_name)
        test_classes = []
        for test_files_with_ext in test_files:
            module_name = test_files_with_ext.rstrip('.py')
            path_to_file = test_files_path + '/' + test_files_with_ext
            imp.load_source(module_name, path_to_file)
            module_members = inspect.getmembers(sys.modules[module_name], inspect.isclass)
            test_classes += [k for k in module_members if module_name in k[1].__module__]

        return test_classes

    @staticmethod
    def _get_test_id(test_method_name):
        test_id = ''
        try:
            test_id = int(test_method_name.split('_')[1].replace('C', ''))
        finally:
            return test_id

    def get_suite_from_test_ids(self, test_ids):
        """

        :param test_ids:
        :return:
        """
        all_test_classes = self.get_test_classes('Suite')

        found_test_with_class = {}
        found_test_count = 0
        for test_class in all_test_classes:
            test_pair = test_class[1].__dict__

            test_methods = [test_method for test_method in test_pair.keys() if 'test_C' in test_method]
            matched_tests = [matched for matched in test_methods if self._get_test_id(matched) in test_ids]

            for test in matched_tests:
                found_test_with_class.update({test: test_class[1]})
            found_test_count += len(matched_tests)

            # breaking out when found all expected tests
            if found_test_count == len(test_ids):
                break

        suite = unittest.TestSuite()

        if len(found_test_with_class) == 0:
            PrintMessage('Failed to find test with id: {0}'.format(test_ids))
            return suite

        # to preserve order in which tests were specified, adding tests as they were initially put in
        for test_id in test_ids:
            indices = [i for i, s in enumerate(found_test_with_class.keys()) if str(test_id) in s]
            if len(indices) > 0:
                index = indices[0]
            else:
                PrintMessage("Failed to find test with test id: {0}".format(test_id))
                continue

            test_name = found_test_with_class.keys()[index]
            class_name = found_test_with_class[test_name]

            suite.addTest(class_name(test_name))

        return suite

    def get_suite_from_test_class(self, classes_to_run):
        all_classes = self.get_test_classes('Suite')

        def match(class_x, class_bunch): return[x for x in class_bunch if class_x.lower() in x[0].lower()]

        all_found = []
        for class_to_run in classes_to_run:
            found = match(class_to_run, all_classes)
            if not found:
                PrintMessage("Not found class name: {0}".format(class_to_run))
                continue

            all_found += found

        suite = unittest.TestSuite()
        loader = unittest.TestLoader()

        if len(all_found) == 0:
            PrintMessage('Failed to find test class with class(s) name: {0}'.format(classes_to_run))
            return suite

        all_found = list(set(all_found))  # casting to set and back to list removes any duplicates

        for class_found in all_found:
            PrintMessage("Executing  tests from test class: {0}".format(class_found[0]))
            suite.addTests(loader.loadTestsFromTestCase(class_found[1]))

        return suite

    # PUBLIC METHODS

    @staticmethod
    def send_report(test_run_id, report_recipients, time_taken=0, test_output_folder=None):
        report_generator = ReportGenerator()
        report_generator.generate_and_send(test_run_id, report_recipients, time_taken, test_output_folder)

    def execute_test_suite(self, with_file_name, build_number, test_run_id):
        test_classes = self.get_test_classes(with_file_name)

        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        for test_class in test_classes:
            suite.addTests(loader.loadTestsFromTestCase(test_class[1]))

        # execute tests
        test_results, time_taken = self.run_test(suite)

        # save results
        self.upload_results(test_results, suite._tests, build_number, test_run_id)

        return time_taken

    def run_selection_send_results(self,
                                   run_id,
                                   build_number,
                                   test_ids,
                                   test_class_names,
                                   loop_count,
                                   loop_until_failure=False):
        """
        :param run_id:
        :param build_number:
        :param test_ids:
        :param test_class_names:
        :param loop_count: amount of times test selection will be executed, stop execution on failure
        :param loop_until_failure: in conjuntion with loop_count execute test in loop until it fails
        :return:
        """
        if len(test_ids) > 0:
            suite = self.get_suite_from_test_ids(test_ids)
        else:
            suite = self.get_suite_from_test_class(test_class_names)

        # execute tests
        test_results = time_taken = None

        # If LUF is set and loop_count is default 1, then set max loop count to 50
        if loop_until_failure and loop_count == 1:
            loop_count = 50

        test_suite_pass_count = 0
        test_suite_fail_count = 0
        while loop_count > 0:
            test_results, time_taken = self.run_test(suite)
            loop_count -= 1

            if test_results.wasSuccessful():
                test_suite_pass_count += 1
            else:
                test_suite_fail_count += 1

            if loop_until_failure and not test_results.wasSuccessful():
                break

        # save results
        self.upload_results(test_results, suite._tests, build_number, run_id)

        # print test run stats
        stats_message = "\n\n Test suite executed {0} times. Test suite failed {1} times.\n"
        PrintMessage(stats_message.format(test_suite_pass_count+test_suite_fail_count, test_suite_fail_count))

        return time_taken
