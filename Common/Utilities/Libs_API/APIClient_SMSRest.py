#!/usr/bin/env python
import base64
import json
import urllib2
import ast


from ...ConfigFiles.ConfigLoader import ConfigLoader
from ...Utilities.Logging import PrintMessage
from ...Utilities.Libs_API.APIClient_Base import BaseAPIClient
from ...Utilities.Libs_API.APIClient_Base import APIEnum


class APIError(Exception):
    pass


class SMSAPIClient(BaseAPIClient):
    def __init__(self, host_address, sms_user=None):
        """
        base_url: 'https://<CMS IP>/api/'

        :param host_address: CMS IP
        :param sms_user: UserWrapper object
        """
        if sms_user is None:
            connection_details = ConfigLoader.get_general_config('DeviceConnectionDetails')
            user = connection_details["User"]
            password = connection_details["Password"]
        else:
            user = sms_user.name
            password = sms_user.password

        self.auth = base64.b64encode('%s:%s' % (user, password))

        super(SMSAPIClient, self).__init__('https://{0}/api/'.format(host_address))

    @staticmethod
    def _handle_http_error(e, expected_http_code):
        error_content = e.read()

        if error_content and 'error' in error_content:
            error_content = ast.literal_eval(error_content)

            error = '"' + error_content["error"] + '"'
        else:
            error = 'No additional error message received'

        crafted_error_message = 'SMS API returned HTTP {0} ({1})'.format(e.code, error)

        if e.code in expected_http_code:
            PrintMessage(crafted_error_message)
        else:
            raise APIError(crafted_error_message)

    @staticmethod
    def _check_http_codes(expected_http_code, actual_code):
        error_message = "Expected {0} HTTP Code, got {1}".format(expected_http_code, actual_code)
        assert actual_code in expected_http_code, error_message

    def _send_request(self, method, uri, expected_http_code, data=None):
        if type(expected_http_code) == int:
            expected_http_codes = [expected_http_code]
        else:
            expected_http_codes = expected_http_code

        url = self._base_url + uri
        PrintMessage("API > {0} > URL : {1}".format(method, url))

        self._log_request(request_originator='sms',
                          request_type=method,
                          url=url,
                          data=data)

        request = urllib2.Request(url)

        request.add_header('Authorization', 'Basic %s' % self.auth)
        request.add_header('Accept', 'application/json')
        request.add_header('Content-Type', 'application/json')
        request.add_header('Accept', '*/*')

        if method == APIEnum.put:
            request.get_method = lambda: 'PUT'
        elif method == APIEnum.delete:
            request.get_method = lambda: 'DELETE'

        if data:
            request.add_data(json.dumps(data))
            # Disabling printing posted data due to some tests pushing hundreds / thousands records
            # PrintMessage('Post Data: {0}'.format(data))

        try:
            response = self.get_response(request)
            http_code = response.getcode()
            self._check_http_codes(expected_http_codes, http_code)

            response_data = response.read()
            if response_data:
                return json.loads(response_data)

        except urllib2.HTTPError as e:
            self._handle_http_error(e, expected_http_codes)

    def get(self, uri, expected_http_code=(200, 404)):
        return self._send_request(APIEnum.get, uri, expected_http_code)

    def post(self, uri, data, expected_http_code=(200, 201), callback=None):
        """

        :param uri:
        :param data:
        :param expected_http_code:
        :param callback: sms function to wait for pending commits == 0
        :return:
        """
        return_data = self._send_request(APIEnum.post, uri, expected_http_code, data)
        if callback:
            callback()
        return return_data

    def put(self, uri, data, expected_http_code=(200, 201), callback=None):
        """

        :param uri:
        :param data:
        :param expected_http_code:
        :param callback: sms function to wait for pending commits == 0
        :return:
        """
        return_data = self._send_request(APIEnum.put, uri, expected_http_code, data)
        if callback:
            callback()
        return return_data

    def delete(self, uri, data=None, expected_http_code=204, callback=None):
        if not data:
            data = {'body': {}, 'statusCode': '100'}
        return_data = self._send_request(APIEnum.delete, uri, expected_http_code, data)
        if callback:
            callback()
        return return_data
