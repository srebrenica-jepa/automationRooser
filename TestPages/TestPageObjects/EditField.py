#!/usr/bin/env python
from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind
from selenium.webdriver.common.by import By


class EditField(object):

    def __init__(self, webdriver, by_type=By.CSS_SELECTOR, value="input.form-control", index=0):
        web_driver_find = WebdriverFind(webdriver)
        self.element = web_driver_find.find_all(by_type, value)[index]

    def clear(self):
        self.element.clear()

    def send_keys(self, value):
        self.clear()
        self.element.send_keys(value)

    def click(self):
        self.element.click()

    def get_current_value(self):
        return self.element.get_attribute("value")

    def get_inner_text(self):
        return self.element.get_attribute("innerText")
