#!/usr/bin/env python


class WebdriverFind(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver

    def find(self, by_type, value):
        """

        :param by_type:
        :param value:
        :return:
        """

        # might be using webdriver internal re-tries or can implement our own
        # ie check for ajax wheel is present, wait for that to go away first
        elements = self.webdriver.find_elements(by_type, value)

        return elements[0]

    def find_all(self, by_type, value):
        """

        :param by_type:
        :param value:
        :return:
        """

        # might be using webdriver internal re-tries or can implement our own
        # ie check for ajax wheel is present, wait for that to go away first
        elements = self.webdriver.find_elements(by_type, value)

        return elements