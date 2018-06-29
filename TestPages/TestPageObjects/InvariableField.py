#!/usr/bin/env python
from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind


class InvariableField(object):
    def __init__(self, webdriver, by_type, value, index=0):
        web_driver_find = WebdriverFind(webdriver)
        self.element = web_driver_find.find_all(by_type, value)[index]

    def get_html(self):
        return self.element.get_attribute('innerHTML')

    def get_text_without_react(self):
        return self.element.get_attribute('innerHTML').split('<!-- /react-text')[0].split('-->')[1]

    def get_inner_text(self):
        return self.element.get_attribute('innerText')

    def get_value(self):
        return self.element.get_attribute("value")

    def click(self):
        self.element.click()
