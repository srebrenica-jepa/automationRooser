#!/usr/bin/python -u
import urllib
import urllib2
from xml.dom import minidom

import time

from ...Utilities import XMLFunctions
from ...Utilities.Logging import PrintMessage
from ...Utilities.Libs_API.APIClient_Base import BaseAPIClient


class SplunkAPIClient(BaseAPIClient):
    def __init__(self, host, user_name, password):
        self.user_name = user_name
        self.password = password
        self.session_key = None

        super(SplunkAPIClient, self).__init__('https://{0}:8089'.format(host))

        self._set_auth_token()

    def _send_post(self, url, data=None):
        #self._log_request(request_type=)
        request = urllib2.Request(url)
        request.add_header('Content-Type', 'application/json')

        if data:
            request.add_data(urllib.urlencode(data))
        if self.session_key:
            request.add_header('Authorization', 'Splunk %s' % self.session_key)

        return self.get_response(request)

    def _set_auth_token(self):
        if self.session_key:
            return

        url = self._base_url + '/services/auth/login'
        auth_data = {'username': self.user_name, 'password': self.password}
        server_content = self._send_post(url, auth_data).read()

        mini_dom_obj = minidom.parseString(server_content)
        session_key_elements = mini_dom_obj.getElementsByTagName('sessionKey')
        self.session_key = session_key_elements[0].childNodes[0].nodeValue

    def _start_splunk_search(self, search_query):
        if 'search' not in search_query:
            search_query = 'search ' + search_query
        search_query = {'search': search_query}

        search_url = self._base_url + '/services/search/jobs/'
        response = self._send_post(search_url, search_query)

        sids = XMLFunctions.get_value_for_element(response.read(), 'sid')

        return sids[0]

    def _delete_search(self, sid):
        delete_search_url = self._base_url + '/services/search/jobs/{0}'.format(sid)
        self._send_post(delete_search_url)

    def _get_search_result(self, sid):
        try:
            get_results_url = self._base_url + '/services/search/jobs/{0}/results'.format(sid)

            try_count = 0
            while try_count < 200:
                time.sleep(5)
                response = self._send_post(get_results_url)

                http_code = response.getcode()
                if http_code == 204:
                    try_count += 1
                    continue
                elif http_code == 200:
                    return response.read()
                else:
                    print ("unexpected http_code = {0}, returning None".format(http_code))
                    return None

            print ("try_count exceeded max, returning None")
            return
        finally:
            self._delete_search(sid)

    def get_search_results(self, search_query):
        PrintMessage('Running splunk search query: {0}'.format(search_query))
        sid = self._start_splunk_search(search_query)
        search_result = self._get_search_result(sid)

        if search_result:
            return XMLFunctions.get_value_for_element(search_result, 'v')
        return None
