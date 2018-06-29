#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField


class ChangePasswordDialog(object):
    def __init__(self, web_element):
        self.web_element = web_element
        self.wait()

    def wait(self):
        change_password_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'modal-body'))
        WebDriverWait(self.web_element, 10).until(change_password_dialog)

    @property
    def new_password(self):
        return EditField(self.web_element, index=1)

    @property
    def confirm_password(self):
        return EditField(self.web_element, index=2)

    @property
    def update_password_button(self):
        return CTAButton(self.web_element, By.CSS_SELECTOR, ".btn-primary", 1)

