#!/usr/bin/env python
from selenium.common.exceptions import WebDriverException
from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind
from selenium.webdriver.common.by import By
from Common.Utilities.Libs.retry import retry

from TestPages.TestPageObjects.CTAButton import UIException


class RadioButton(object):

    def __init__(self, webdriver, by_type=By.CLASS_NAME, value="radio-label-wrapper", index=0):
        web_driver_find = WebdriverFind(webdriver)
        self.element = web_driver_find.find_all(by_type, value)[index]

    @retry(exceptions=(WebDriverException, UIException), delay=3, tries=15)
    def click(self):
        if not self.element.is_enabled():
            raise UIException('element is not enabled')
        if not self.element.is_displayed():
            raise UIException('element is not displayed')

        self.element.click()
