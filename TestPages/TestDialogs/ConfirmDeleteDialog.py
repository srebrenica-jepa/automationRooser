#!/usr/bin/env pythonn
from TestPages.TestPageObjects.CTAButton import CTAButton

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class ConfirmDeleteDialog(object):
    def __init__(self, web_element):
        self.web_element = web_element
        self.wait()

    def wait(self):
        """
        Added try and catch, because sometimes confirm delete dialogs are in form of Modal and sometimes as AJS
        and it is very inconsistent.
        """
        try:
            confirm_modal_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'btn-default'))
            WebDriverWait(self.web_element, 2).until(confirm_modal_dialog)
        except TimeoutException:
            confirm_ajs_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'ajs-cancel'))
            WebDriverWait(self.web_element, 2).until(confirm_ajs_dialog)

    def wait_for_system(self):
        confirm_system_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'modal-body'))
        WebDriverWait(self.web_element, 10).until(confirm_system_dialog)

    def wait_for_ajs_dialog(self):
        confirm_ajs_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'ajs-body'))
        WebDriverWait(self.web_element, 10).until(confirm_ajs_dialog)

    def wait_dialog(self):
        confirm_dialog = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.sweet-alert'))

    @property
    def confirm_delete(self):
        return CTAButton(self.web_element, By.CSS_SELECTOR, ".btn.btn-lg.btn-danger")

    @property
    def cancel_delete(self):
        return CTAButton(self.web_element, By.CSS_SELECTOR, ".btn-default")
