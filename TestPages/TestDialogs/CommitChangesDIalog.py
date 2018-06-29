#!/usr/bin/env python
from TestPages.TestPageObjects.CTAButton import CTAButton
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CommitChangesDialog(object):
    def __init__(self, web_element):
        self.web_element = web_element
        self.wait()

    def wait(self):
        commit_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, "modal-footer"))
        WebDriverWait(self.web_element, 10).until(commit_dialog)

    def wait_for_system(self):
        confirm_system_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'modal-body'))
        WebDriverWait(self.web_element, 10).until(confirm_system_dialog)

    @property
    def cancel_button(self):
        return CTAButton(self.web_element, By.CSS_SELECTOR, "button.btn.btn-default")

    @property
    def discard_button(self):
        return CTAButton(self.web_element, By.CSS_SELECTOR, "button.btn.btn-primary", 0)

    @property
    def commit_button(self):
        return CTAButton(self.web_element, By.CSS_SELECTOR, "button.btn.btn-primary", 1)
