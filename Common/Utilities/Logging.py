#!/usr/bin/env python
import logging
import json
import sys
import os

from datetime import datetime
from time import strftime

from ..Utilities import DiskTools
MESSAGE_FORMAT = "{0} {1}"


class LoggingLevel(object):
    info = 'info'
    warning = 'warning'
    error = 'error'


def LogAPIRequest(request_originator, request_type, url, data):
    logger = logging.getLogger('apiLog')
    time_stamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S.%f")[:-4]
    message_to_log = MESSAGE_FORMAT.format(time_stamp, '{0} {1} request at url: {2}'.format(request_originator,
                                                                                            request_type,
                                                                                            url))
    logger.info(message_to_log)
    if data:
        try:
            message_to_log = json.dumps(data, indent=4, sort_keys=True)
            logger.info(message_to_log)
        except (ValueError, TypeError):
            PrintMessage('FAILED to process message in PrintAPIRequest:{0}'.format(data), level=LoggingLevel.error)


def PrintMessage(message, level=LoggingLevel.info):
    time_stamp = datetime.now().strftime("%d-%b-%Y %H:%M:%S.%f")[:-4]
    message_to_log = MESSAGE_FORMAT.format(time_stamp, message)

    logger = logging.getLogger('testLog')
    if len(logger.handlers) > 0:
        if level == LoggingLevel.error:
            logger.error(message_to_log)
        elif level == LoggingLevel.warning:
            logger.warning(message_to_log)
        else:
            logger.info(message_to_log)
    else:
        print message_to_log


class StreamToLogger(object):
    def __init__(self, log_drop_folder=None, config_name=None):
        """
        This class can be created multiple times, have
        :param log_drop_folder:
        :param config_name:
        """
        self.log_id_env = config_name
        self.datetime_stamp = strftime('%b%d_%H%M')
        self.terminal = sys.stdout

        self._create_log_drop_folder(log_drop_folder)
        self._set_api_log()
        self._set_test_log()

    def __del__(self):
        if self.log_file_handler:
            self.log_file_handler.close()

    def _create_log_drop_folder(self, log_drop_folder):
        self.log_drop_folder = self._get_log_folder(log_drop_folder)

        DiskTools.create_folder(self.log_drop_folder)
        assert os.path.exists(self.log_drop_folder), "Expected valid path, got: {0}".format(self.log_drop_folder)

    @staticmethod
    def _get_log_folder(log_drop_folder):
        if log_drop_folder:
            return log_drop_folder
        else:
            return './testLogging/'

    def _get_log_file_name(self, prefix):
        """
        Builds up a log file name based on the prefix and presence/ absence of log_id_dev (i.e.: lyra_kvm)
        :param prefix: either test or rest_api
        :return:
        """
        file_name = '{0}_{1}.log'.format(prefix, self.datetime_stamp)
        if self.log_id_env:
            file_name = '{0}_{1}'.format(self.log_id_env, file_name)
        return file_name

    def _set_test_log(self):
        """
        Standard log, through a localy created stream
        :return:
        """
        logger = logging.getLogger('testLog')

        self.log_file_handler = open(self.log_drop_folder + self._get_log_file_name('test'), "w")
        logger.setLevel(logging.INFO)
        logger.addHandler(logging.StreamHandler(self))

    def _set_api_log(self):
        """
        Standard API log, created through Python logging library
        :return:
        """
        logger = logging.getLogger('apiLog')

        handler = logging.FileHandler(self.log_drop_folder + self._get_log_file_name('rest_api'))
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    def write(self, buf):
        self.terminal.write(buf)
        self.log_file_handler.write(buf)

    def flush(self):
        self.terminal.flush()
        self.log_file_handler.flush()
