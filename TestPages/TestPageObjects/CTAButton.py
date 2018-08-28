#!/usr/bin/env python
from selenium.common.exceptions import WebDriverException
from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind
from Common.Utilities.Libs.retry import retry
from Common.Utilities.Logging import PrintMessage
from TestPages.TestPageObjects.InvariableField import InvariableField


class UIException(WebDriverException):
    pass


class Button(object):
    def __init__(self, webdriver):
        self.web_driver_find = WebdriverFind(webdriver)
        self.element = None

    def print_attributes(self):
        attrs = self.web_driver_find.webdriver.execute_script('var items = {}; for (index = 0; index < arguments[0].'
                                                              'attributes.length; ++index) { items[arguments[0].'
                                                              'attributes[index].name] = arguments[0].'
                                                              'attributes[index].value }; return items;', self.element)
        PrintMessage('elem_attrib:' + str(attrs), include_time_stamp=False)

    @retry(exceptions=(WebDriverException, UIException), delay=10, tries=15)
    def click(self):
        if not self.element.is_enabled():
            self.print_attributes()
            raise UIException('element is not enabled')
        if not self.element.is_displayed():
            self.print_attributes()
            raise UIException('element is not displayed')

        self.element.click()

    def send_keys(self, value):
        self.element.clear()
        self.element.send_keys(value)

    def send_keys_no_clear(self, value):
        self.element.send_keys(value)

    def enter(self, value):
        self.element.send_keys(value)

    def get_title(self):
        return self.element.get_attribute('title')


class CTAButton(Button, InvariableField):
    def __init__(self, webdriver, by_type, value, index=0):
        super(CTAButton, self).__init__(webdriver)
        self.element = self.web_driver_find.find_all(by_type, value)[index]



