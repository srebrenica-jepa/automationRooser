#!/usr/bin/env python

import exceptions


class FailedLoginError(exceptions.StandardError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super(FailedLoginError, self).__init__()
        pass


class TestError(exceptions.StandardError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super(TestError, self).__init__()
        pass


class SplunkNoResults(exceptions.StandardError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super(SplunkNoResults, self).__init__()
        pass


class SplunkUnexpectedResults(exceptions.StandardError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super(SplunkUnexpectedResults, self).__init__()
        pass


class CLINoResults(exceptions.StandardError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super(CLINoResults, self).__init__()
        pass


class DeploymentException(exceptions.StandardError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super(DeploymentException, self).__init__()
        pass


class WaiterNoResults(exceptions.StandardError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super(WaiterNoResults, self).__init__()
        pass


class VMNotFound(exceptions.StandardError):
    def __init__(self, *args, **kwargs):  # real signature unknown
        super(VMNotFound, self).__init__()
        pass
