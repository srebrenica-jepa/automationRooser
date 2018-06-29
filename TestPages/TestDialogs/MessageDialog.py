#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind


class MessageDialog(object):
    def __init__(self, web_element, web_element_index=0):
        self.web_element = web_element
        web_driver_find = WebdriverFind(web_element)
        self.element = web_driver_find.find_all(by_type=By.CSS_SELECTOR, value='.ajs-message')[web_element_index]
        self.wait()

    def wait(self):
        confirm_ajs_dialog = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ajs-message'))
        WebDriverWait(self.web_element, 300).until(confirm_ajs_dialog)

    def get_inner_text(self):
        return self.element.get_attribute('innerText')
