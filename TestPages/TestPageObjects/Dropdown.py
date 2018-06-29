#!/usr/bin/env python

from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.InvariableField import InvariableField
from selenium.webdriver.common.keys import Keys


class Dropdown(object):
    def __init__(self, webdriver, by_type=By.CLASS_NAME, value="Select-control", index=0):
        self.webdriver = webdriver
        web_driver_find = WebdriverFind(webdriver)
        self.element = web_driver_find.find_all(by_type, value)[index]
        self.index = index

    def wait(self):
        dropdown = EC.visibility_of_element_located((By.CLASS_NAME, 'Select-control'))
        WebDriverWait(self.webdriver, 10).until(dropdown)

    def wait_for_dropdown(self):
        menu_options = EC.visibility_of_element_located((By.CLASS_NAME, 'Select-input'))
        WebDriverWait(self.webdriver, 10).until(menu_options)

    def select_input(self, value=None):
        self.arrow.click()
        self.enter_input.send_keys(value)
        self.enter_input.enter(Keys.ENTER)

    def click(self):
        self.element.click()

    def get_value(self):
        return self.element.get_attribute('innerHTML')

    @property
    def arrow(self):
        return CTAButton(self.webdriver, By.CLASS_NAME, "Select-arrow-zone", self.index)

    @property
    def enter_input(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "input[role='combobox']", self.index)

    @property
    def current_value(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, "span[role='option']", self.index).get_html()


class DropdownMenu(Dropdown):
    def __init__(self, webdriver, by_type=By.CSS_SELECTOR, value=".dropdown", index=0,
                 by_type_of_option=By.CSS_SELECTOR, value_of_option=".dropdown > ul > li", index_of_option=0):
        super(DropdownMenu, self).__init__(webdriver, by_type, value, index)
        self.option = WebdriverFind(webdriver).find_all(by_type_of_option, value_of_option)[index_of_option]
        self.index_of_option = index_of_option

    def wait_for_dropdown(self):
        menu_options = EC.visibility_of_element_located((By.CSS_SELECTOR, '.dropdown'))
        WebDriverWait(self.webdriver, 10).until(menu_options)

    def click(self):
        self.wait_for_dropdown()
        self.element.click()

    def select_input(self, value=None):
        self.arrow.click()
        self.wait_for_dropdown()
        self.enter_input.click()

    @property
    def arrow(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "span.dropdown > button > span", self.index)

    @property
    def enter_input(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "span.dropdown > ul > li", self.index_of_option)


class DropdownSelect(object):
    def __init__(self, webdriver, by_type=By.CSS_SELECTOR, value=".form-control.truncate", index=0, by_type_of_option=By.CSS_SELECTOR, value_of_option=".form-control.truncate > option", index_of_option=0):
        self.webdriver = webdriver
        web_driver_find = WebdriverFind(webdriver)
        self.element = web_driver_find.find_all(by_type, value)[index]
        self.index = index
        self.option = WebdriverFind(webdriver).find_all(by_type_of_option, value_of_option)[index_of_option]
        self.index_of_option = index_of_option

    def wait_for_dropdown(self):
        menu_options = EC.visibility_of_element_located((By.CSS_SELECTOR, '.form-control.truncate'))
        WebDriverWait(self.webdriver, 10).until(menu_options)

    def select_input(self, value=None):
        self.arrow.click()
        self.wait_for_dropdown()
        self.enter_input.click()

    def get_value(self):
        return self.element.get_attribute("value")

    @property
    def arrow(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".form-control.truncate", self.index)

    @property
    def enter_input(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".form-control.truncate > option", self.index_of_option)



