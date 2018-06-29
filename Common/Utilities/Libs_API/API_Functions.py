#!/usr/bin/env python


class APIWrapper(object):
    def __init__(self, api_client):
        self.api_client = api_client

    def get_v1(self, uri, expected_http_code=(200, 404)):
        versioned_uri = uri.replace('latest', 'v1')
        return self.api_client.get(versioned_uri,
                                   expected_http_code=expected_http_code)

    def post_v1(self, uri, data, expected_http_code=(200, 201), callback=None):
        versioned_uri = uri.replace('latest', 'v1')
        return self.api_client.post(versioned_uri,
                                    data=data,
                                    expected_http_code=expected_http_code,
                                    callback=callback)

    def put_v1(self, uri, data, expected_http_code=(200, 201), callback=None):
        versioned_uri = uri.replace('latest', 'v1')
        return self.api_client.put(versioned_uri,
                                   data=data,
                                   expected_http_code=expected_http_code,
                                   callback=callback)

    def delete_v1(self, uri, expected_http_code=204, callback=None):
        versioned_uri = uri.replace('latest', 'v1')
        return self.api_client.delete(versioned_uri,
                                      expected_http_code=expected_http_code,
                                      callback=callback)

    def get_v2(self, uri, expected_http_code=(200, 404)):
        versioned_uri = uri.replace('latest', 'v2')
        return self.api_client.get(versioned_uri,
                                   expected_http_code=expected_http_code)

    def post_v2(self, uri, data, expected_http_code=(200, 201), callback=None):
        versioned_uri = uri.replace('latest', 'v2')
        return self.api_client.post(versioned_uri,
                                    data=data,
                                    expected_http_code=expected_http_code,
                                    callback=callback)

    def put_v2(self, uri, data, expected_http_code=(200, 201), callback=None):
        versioned_uri = uri.replace('latest', 'v2')
        return self.api_client.put(versioned_uri,
                                   data=data,
                                   expected_http_code=expected_http_code,
                                   callback=callback)

    def delete_v2(self, uri, data=None, expected_http_code=204, callback=None):
        versioned_uri = uri.replace('latest', 'v2')
        return self.api_client.delete(versioned_uri,
                                      data=data,
                                      expected_http_code=expected_http_code,
                                      callback=callback)


