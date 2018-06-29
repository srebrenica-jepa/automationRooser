#!/usr/bin/env python
import sys
import ssl
import urllib2

from Common.Utilities.Logging import LogAPIRequest


class APIEnum(object):
    post = 'POST'
    put = 'PUT'
    get = 'GET'
    delete = 'DELETE'


class BaseAPIClient(object):
    def __init__(self, base_url):
        """
        :param base_url: 'https://<CMS IP>/api/'
        """
        self._base_url = base_url

    @staticmethod
    def get_response(request):
        """
        sys.version_info returns python version (major, minor, build)
        we do not want SSL context to be used with python where build is less than 13
        :param request:
        :return:
        """
        if sys.version_info[0] == 2 and sys.version_info[2] < 13:
            return urllib2.urlopen(request)
        else:
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            return urllib2.urlopen(request, context=context)

    @staticmethod
    def _log_request(request_originator, request_type, url, data):
        LogAPIRequest(request_originator, request_type, url, data)
