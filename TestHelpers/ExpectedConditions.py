#!/usr/bin/env python
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import StaleElementReferenceException


def find_elements(driver, by):
    try:
        return driver.find_elements(*by)
    except WebDriverException as e:
        raise e


class text_to_be_present_in_element(object):
    """ An expectation for checking if the given text is present in the
    specified element.
    locator, text
    """
    def __init__(self, locator, text_, element_index=0):
        self.locator = locator
        self.text = text_
        self.element_index = element_index

    def __call__(self, driver):
        try:
            element_text = find_elements(driver, self.locator)[self.element_index].text
            return self.text in element_text
        except StaleElementReferenceException:
            return False


