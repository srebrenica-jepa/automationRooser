#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind
from TestPages.TestPageObjects.CTAButton import CTAButton


class ConfirmationMessageDialog(object):
    def __init__(self, web_element):
        self.web_element = web_element
        self.wait()

    def wait(self):
        try:
            confirm_modal_dialog = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.sweet-alert'))
            WebDriverWait(self.web_element, 2).until(confirm_modal_dialog)
        except TimeoutException:
            confirm_ajs_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'ajs-cancel'))
            WebDriverWait(self.web_element, 2).until(confirm_ajs_dialog)

    @property
    def ok_button(self):
        return CTAButton(self.web_element, By.CSS_SELECTOR, ".btn.btn-lg.btn-primary")
