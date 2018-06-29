#!/usr/bin/env python

from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.Utilities.Enums import TestResult
from Common.Utilities.Libs_API.APIClient_TestRail import TestRailAPIClient
from Common.Utilities.Logging import PrintMessage
from Common.TestExecute import TestFuncs


# Converts UnitTest results to format accepted by Test Rail
# Uploads test results to Test Rail
class TestRailResultUploader(object):
    def __init__(self, test_run_id, tested_build_version):
        self.tested_build_version = tested_build_version
        self.test_run_id = test_run_id

        test_rail_info = ConfigLoader.get_test_report_config()
        self.test_rail = TestRailAPIClient(
            test_rail_info['URL'],
            test_rail_info['User'],
            test_rail_info['Password'])

    # formatting: test_C26315_UDP_Fragments_Bit (__main__.Test_RuleChecking) into something more usable
    @staticmethod
    def _get_test_details(test_full_name):
        test_name = test_id = class_name = None
        try:
            test_full_name = str(test_full_name)
            test_name, module_name = test_full_name.split(' ')
            test_id = TestFuncs.test_id_from_test_name(test_name)
            file_name, class_name = module_name.strip('()').split('.')

            return test_name, test_id, class_name

        except:
            PrintMessage("_get_test_details > failed parsing test with name: {0}".format(test_full_name))

        return test_name, test_id, class_name

    def _get_test_ids(self, test_cases):
        test_cases_clean = []

        for test_case in test_cases:
            test_name, test_id, class_name = self._get_test_details(test_case)

            # if failed to get the test_case_id, skip and continue on subsequent test
            # the exception will be logged in _get_test_details method
            if test_id is None:
                continue

            test_cases_clean.append(test_id)

        return test_cases_clean

    # get last 7 results from the test
    # results are ordered from most recent to oldest
    # returns [latest_defect, fail_count]
    def _get_most_recent_defect_id(self, test_case_id, limit=7):
        test_results = self.test_rail.get_test_result_test_case(self.test_run_id,
                                                                test_case_id,
                                                                limit)
        if test_results:
            for test_result in test_results:
                if test_result['status_id'] == TestResult.Passed:
                    return ''
                if test_result['defects']:
                    return test_result['defects']

        return ''

    @staticmethod
    def _get_test_result_comment(failed_test):
        """
        failed_test[1] is the Traceback
        :param failed_test:
        :return:
        """
        test_traceback = str(failed_test[1])
        test_result = failed_test[0]
        comment_with_result = '{0} \n\r {1}'

        if hasattr(test_result, 'splunk_url'):
            return comment_with_result.format(test_result.splunk_url, test_traceback)

        elif hasattr(test_result, '_resultForDoCleanups'):
            if hasattr(test_result._resultForDoCleanups, 'screenshot_url'):
                return comment_with_result.format(test_result._resultForDoCleanups.screenshot_url, test_traceback)

        return test_traceback

    def _process_failed_tests(self, failed_tests, test_status):
        """
        processes failed, errored and skipped tests
        :param failed_tests:
        :param test_status:
        :return:
        """
        if len(failed_tests) == 0:
            return dict()

        test_results = dict()

        for failed_test in failed_tests:
            test_full_name = str(failed_test[0])
            test_comment = self._get_test_result_comment(failed_test)

            test_name, test_case_id, class_name = self._get_test_details(test_full_name)

            # if failed to get the test_case_id, skip and continue on subsequent test
            # the exception will be logged in _get_test_details method
            if test_case_id is None:
                continue

            latest_defect = self._get_most_recent_defect_id(test_case_id)

            test_results.update({test_case_id: [test_status, test_comment, latest_defect]})

        return test_results

    def _process_passed_tests(self, test_results_processed, tests_cases):
        all_test_ids = self._get_test_ids(tests_cases)
        passed_test_ids = list(set(test_results_processed.keys()).symmetric_difference(all_test_ids))

        if len(passed_test_ids) == 0:
            return dict()

        test_results = dict()

        for passed_test_id in passed_test_ids:
            test_results.update({passed_test_id: [TestResult.Passed, 'Thumbs Up', '']})

        return test_results

    def process_and_upload(self, test_results, tests_cases):
        test_results_processed = dict()

        # Processing 3 lists of results obtained from unittest [failures, errors, skipped]
        test_results_processed.update(self._process_failed_tests(test_results.failures, TestResult.Failed))
        test_results_processed.update(self._process_failed_tests(test_results.errors, TestResult.Failed))
        test_results_processed.update(self._process_failed_tests(test_results.skipped, TestResult.Blocked))
        test_results_processed.update(self._process_passed_tests(test_results_processed, tests_cases))

        self.test_rail.post_test_results(self.tested_build_version, self.test_run_id, test_results_processed)
