#
# TestRail API binding for Python 2.x (API v2, available since
# TestRail 3.0)
#
# Learn more:
#
# http://docs.gurock.com/testrail-api2/start
# http://docs.gurock.com/testrail-api2/accessing
#
# Copyright Gurock Software GmbH. See license.md for details.
#

import base64
import json
import traceback
import urllib2

from ...Utilities.Logging import PrintMessage
from ...Utilities.Libs_API.APIClient_Base import BaseAPIClient


class TestRailAPIClient(BaseAPIClient):
    def __init__(self, host_address, user_name, password):
        self.user = user_name
        self.password = password
        if not host_address.endswith('/'):
            host_address += '/'

        super(TestRailAPIClient, self).__init__(host_address + 'index.php?/api/v2/')

    def _send_request(self, method, uri, data=None):
        url = self._base_url + uri
        request = urllib2.Request(url)
        if method == 'POST':
            request.add_data(json.dumps(data))
        auth = base64.b64encode('%s:%s' % (self.user, self.password))
        request.add_header('Authorization', 'Basic %s' % auth)
        request.add_header('Content-Type', 'application/json')

        e = None
        response_data = self.get_response(request).read()

        if response_data:
            result = json.loads(response_data)
        else:
            result = {}

        if e is not None:
            if result and 'error' in result:
                error = '"' + result['error'] + '"'
            else:
                error = 'No additional error message received'
            raise APIError('TestRail API returned HTTP %s (%s)' %
                           (e.code, error))

        return result

    def get(self, uri):
        return self._send_request('GET', uri)

    def post(self, uri, data):
        return self._send_request('POST', uri, data)

    #
    # expected data in dictionary format:
    # {'version': <string>, 'status_id': <string>, 'comment': <string>}
    #

    def _post_results_for_test_case(self, test_run_id, test_id, data):
        rest_url = 'add_result_for_case/{0}/{1}'.format(test_run_id, test_id)

        try:
            self.post(rest_url, data)

        except urllib2.HTTPError:
            PrintMessage("Test case: {0} not included in test run: {1}.".format(test_id, test_run_id))

        except APIError:
            PrintMessage(traceback.format_exc())
            PrintMessage('Data attempted to send: {0}'.format(data))
            PrintMessage("Failed to upload data for test case: {0} and run: {1}".format(test_id, test_run_id))

    # expects in all_test_results
    # index 0: test status id (pass / failed etc)
    # index 1: test comment
    # index 2: defect
    def post_test_results(self, tested_build_version, test_run_id, all_test_results):
        for test_id in all_test_results:
            test_status_id = all_test_results[test_id][0]
            test_comment = all_test_results[test_id][1]
            test_defect = all_test_results[test_id][2]

            data = {'version': str(tested_build_version),
                    'defects': test_defect,
                    'status_id': test_status_id,
                    'comment': test_comment}
            self._post_results_for_test_case(test_run_id, test_id, data)

    def get_list_of_tests_for_run_id(self, test_run_id, limit=None):
        assert type(test_run_id) == int, 'Expected int value for the test run id.'

        rest_url = 'get_tests/{0}'.format(test_run_id)
        if limit is not None:
            rest_url += '&limit={0}'.format(limit)
        return self.get(rest_url)

    #
    # test_id =/= test_case_id
    #
    def get_test_result(self, test_id, limit=None):
        """

        :param test_id:
        :param limit:
        :return: results include:
         assignedto_id
         comment
         created_by
         created_on
         custom_step_results []
         defects
         elapsed
         id
         status_id
         test_id
         version
        """
        rest_url = 'get_results/{0}'.format(test_id)
        if limit:
            rest_url += '&limit={0}'.format(limit)

        return self.get(rest_url)

    #
    # test_id =/= test_case_id
    #
    def get_test_result_test_case(self, test_run_id, test_case_id, limit=None):
        rest_url = 'get_results_for_case/{0}/{1}'.format(test_run_id, test_case_id)
        if limit:
            rest_url += '&limit={0}'.format(limit)

        try:
            return self.get(rest_url)
        except (APIError, urllib2.HTTPError):
            PrintMessage("Failed getting data for test case: {0} from test run: {1}".format(test_case_id, test_run_id))

            return None

    def get_run_info(self, run_id):
        assert type(run_id) == int, 'Expected int value for the test run id.'

        rest_url = 'get_run/{0}'.format(run_id)

        return self.get(rest_url)

    def get_mile_stone_text(self, test_run_id):
        run_info = self.get_run_info(test_run_id)
        mile_stone_url = 'get_milestone/{0}'.format(run_info['milestone_id'])

        return self.get(mile_stone_url)['name']


class APIError(Exception):
    pass
