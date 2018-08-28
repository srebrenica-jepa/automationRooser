#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.PageEnums import State
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.CheckBox import CheckBox
from TestPages.PageActions.NotificationVerifier import NotificationVerifier
from TestPages.PageEnums import CheckOneBox


class TransportsAddDialog(NotificationVerifier):
    def __init__(self, webdriver):
        super(TransportsAddDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def add_entry_and_save(self, name, weight=None, shipping=CheckOneBox.no):
        self.wait()

        self.name.send_keys(name)
        if weight:
            self.minimum_weight.send_keys(weight)

        if shipping==CheckOneBox.yes:
            self.shipping.click()

        self.save_button.click()

    @property
    def name(self):
        return EditField(self.webdriver, index=0)

    @property
    def minimum_weight(self):
        return EditField(self.webdriver, index=1)

    @property
    def shipping(self):
        return CheckBox(self.webdriver, By.CSS_SELECTOR, ".form-check-input")

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-success")
