#! /usr/bin/python
from collections import Counter

from Common.ConfigFiles.ConfigLoader import ConfigLoader
from Common.TestReporting import Constants as Const
from Common.TestReporting.MailClient import send_mail
from Common.Utilities.Enums import TestResult
from Common.Utilities.Libs_API.APIClient_TestRail import TestRailAPIClient
from Common.Utilities.Logging import PrintMessage

test_status_to_result = {TestResult.Passed: 'Passed',
                         TestResult.Blocked: 'Blocked',
                         TestResult.Untested: 'Untested',
                         TestResult.Retest: 'Retest',
                         TestResult.Failed: 'Failed',
                         TestResult.Pass_wCon: 'Pass*',
                         None: 'Untested'}


class ReportGenerator(object):
    def __init__(self):
        test_rail_info = ConfigLoader.get_test_report_config()
        self.test_rail = TestRailAPIClient(
            test_rail_info['URL'],
            test_rail_info['User'],
            test_rail_info['Password'])

        self.test_sections = {}
        self.build_number = None

    # returns a list of dictionaries, returned fields:
    # assignedto_id
    # comment
    # status_id
    # title
    # created_by
    # elapsed
    # created_on
    # version
    # defects
    # test_id
    # id
    def _get_test_results_for_run(self, test_run_id):
        all_test_cases = self.test_rail.get_list_of_tests_for_run_id(test_run_id)
        PrintMessage("Test count: {0} in test run : {1}".format(len(all_test_cases), test_run_id))

        expanded_test_rail_results = []
        for test_case in all_test_cases:
            test_rail_results = self.test_rail.get_test_result(test_case['id'], limit=7)

            fail_count = 0
            history = []

            for idx in xrange(len(test_rail_results)):
                test_result = test_rail_results[idx]

                if test_result['status_id'] == TestResult.Failed:
                    fail_count += 1

                history.append(test_result['status_id'])

            history.reverse()  # so results are displayed from right (most recent) to left (oldest)
            if test_rail_results:
                test_rail_results[0].update({'fail_count': fail_count})
                test_rail_results[0].update({'history': history})
                test_rail_results[0].update({'title': test_case['title']})
                test_rail_results[0].update({'case_id': test_case['case_id']})
                expanded_test_rail_results.append(test_rail_results[0])
            else:
                continue

        PrintMessage("Test execution count: {0} in test run : {1}".format(len(all_test_cases), test_run_id))
        return expanded_test_rail_results

    def _get_test_result_history(self, test_history):
        entries = ''
        for result in test_history:
            if result == TestResult.Passed:
                color = '#0BC200'
            elif result == TestResult.Blocked:
                color = '#8c8c8c'
            elif result == TestResult.Failed:
                color = '#ff3300'
            else:
                color = '#f2f2f2'

            entries += Const.RESULT_HISTORY_ENTRY.format(color)

        return Const.RESULT_HISTORY.format(entries)

    def _get_result_and_color_from_status_code(self, status_code):
        if status_code == TestResult.Passed:
            color = '#33cc33'
        elif status_code == TestResult.Blocked:
            color = '#8c8c8c'
        elif status_code == TestResult.Failed:
            color = '#ff3300'
        else:
            color = '#f2f2f2'

        return test_status_to_result[status_code], color

    def _get_section_id(self, case_id):
        """
        retrieves section id and parents to build a full name
        bottom level section id is the identifier for each full name
        :param case_id:
        :return:
        """
        rest_url = 'get_case/{0}'.format(case_id)
        result = self.test_rail.get(rest_url)
        section_id = result['section_id']

        if section_id in self.test_sections:
            return section_id

        section_full_name = None
        loop_section_id = section_id
        get_section_url = 'get_section/{0}'
        while True:
            url_to_use = get_section_url.format(loop_section_id)
            result = self.test_rail.get(url_to_use)

            if result:
                if section_full_name:
                    section_full_name = result['name'] + ' - ' + section_full_name
                else:
                    section_full_name = result['name']

                if result['parent_id']:
                    loop_section_id = result['parent_id']
                else:
                    break

        self.test_sections[section_id] = section_full_name

        return section_id

    def _process_test_rail_results(self, test_rail_results):
        """
        process test rails results into manageable data structure containing only details we're interested in
        """

        test_results_by_section = {}
        for test_rail_result in test_rail_results:
            test_result = {}
            test_history = self._get_test_result_history(test_rail_result['history'])

            test_result['version'] = test_rail_result['version']
            test_result['test_id'] = 'C' + str(test_rail_result['case_id'])
            test_result['test_title'] = Const.TEST_TITLE.format(test_rail_result['test_id'], test_rail_result['title'])

            test_pass_state, cell_color = self._get_result_and_color_from_status_code(test_rail_result['status_id'])
            test_result['test_pass_state'] = test_pass_state
            test_result['cell_color'] = cell_color
            test_result['test_history'] = test_history

            section_id = self._get_section_id(test_rail_result['case_id'])

            if section_id not in test_results_by_section:
                test_results_by_section[section_id] = []
            test_results_by_section[section_id].append(test_result)

        return test_results_by_section

    def _update_results_table_with_all_tests(self, test_rail_results):
        version_count = Counter()

        test_results_by_section = self._process_test_rail_results(test_rail_results)

        report_rows = []
        for section_id in test_results_by_section:
            report_rows.append(Const.ROW_TEMPLATE_SECTION.format(self.test_sections[section_id]))

            for test_result in test_results_by_section[section_id]:

                version_count[test_result['version']] += 1

                row = Const.ROW_TEMPLATE_ALL_RESULTS.format(test_result['test_id'],
                                                            test_result['version'],
                                                            test_result['test_title'],
                                                            test_result['cell_color'],
                                                            test_result['test_pass_state'],
                                                            test_result['test_history'])
                report_rows.append(row)

        self.build_number = version_count.most_common()[0][0]

        return Const.TABLE_TEMPLATE_ALL_RESULTS.format(''.join(report_rows))

    def _update_results_table_with_failed_tests(self, test_rail_results):
        report_rows = []
        for test_rail_result in test_rail_results:
            if test_rail_result['status_id'] != TestResult.Failed:
                continue

            test_title = Const.TEST_TITLE.format(test_rail_result['test_id'], test_rail_result['title'])

            test_fail_count = test_rail_result['fail_count']
            defects = test_rail_result['defects']

            if defects:
                html_defect = Const.BUG_ID.format(defects)
            else:
                html_defect = ''

            test_history = self._get_test_result_history(test_rail_result['history'])

            row = Const.ROW_TEMPLATE_FAILURES.format('C' + str(test_rail_result['case_id']),
                                                     test_rail_result['version'],
                                                     test_title,
                                                     html_defect,
                                                     test_fail_count,
                                                     test_history)
            report_rows.append(row)

        if len(report_rows) > 0:
            return Const.TABLE_TEMPLATE_FAILURES.format(''.join(report_rows),)
        else:
            return ''

    # expects single test result per test
    def _create_test_report(self, run_id, run_stats_html, test_output_folder_href):
        test_rail_results = self._get_test_results_for_run(run_id)

        passed_table = self._update_results_table_with_all_tests(test_rail_results)
        failures_table = self._update_results_table_with_failed_tests(test_rail_results)

        self.test_report = Const.REPORT_TEMPLATE.format(run_stats_html,
                                                        test_output_folder_href,
                                                        failures_table,
                                                        passed_table)

    @staticmethod
    def _format_time_taken(time_taken):
        hours = int(time_taken / 3600)
        minutes = int((time_taken - (hours * 3600))/60)

        formatted_message = Const.TIME_TAKEN.format(hours, minutes)
        PrintMessage('TimeTaken: {0}'.format(formatted_message))
        return formatted_message

    def _get_full_version(self, run_id):
        milestone_name = self.test_rail.get_mile_stone_text(run_id)

        return "{0} build {1}".format(milestone_name, self.build_number)

    @staticmethod
    def _get_report_output_folder_href(test_output_folder):
        """

        :param test_output_folder: i.e.  /sandbox/qadrop/automation_logs/gx/Mar29_1636/
        :return: http://hades.corero.com/automation/gx/Mar29_1636
        """
        if test_output_folder:
            # test_log_folder is expected to be '/gx/Mar29_1636/'
            server_path, test_log_folder = Const.split_log_drop_path(test_output_folder)
            return Const.TEST_FILE_FOLDER.format(Const.HADES_URL_PATH, test_log_folder)
        else:
            return ''

    def generate_and_send(self, run_id, recipients, time_taken, test_output_folder=None):
        self.build_number = None

        run_info = self.test_rail.get_run_info(run_id)
        passed_count = run_info['passed_count']
        failed_count = run_info['failed_count']
        blocked_count = run_info['blocked_count']

        total_pass_count = passed_count + run_info['custom_status1_count']
        total_count_ex_blocked = total_pass_count + failed_count

        pass_rate = round(float(total_pass_count) / total_count_ex_blocked * 100, 2)

        run_stats_html = Const.STATS_TEMPLATE.format(total_pass_count + failed_count + blocked_count,
                                                     passed_count,
                                                     failed_count,
                                                     blocked_count,
                                                     passed_count + failed_count,
                                                     pass_rate,
                                                     self._format_time_taken(time_taken))

        self._create_test_report(run_id=run_id,
                                 run_stats_html=run_stats_html,
                                 test_output_folder_href=self._get_report_output_folder_href(test_output_folder))

        mail_title = Const.EMAIL_TITLE.format(run_info['name'],
                                              pass_rate,
                                              total_pass_count,
                                              total_count_ex_blocked,
                                              self._get_full_version(run_id))

        send_mail(subject=mail_title,
                  html_body=self.test_report,
                  m_from='testrail-automation@corero.com',
                  m_to=recipients)
