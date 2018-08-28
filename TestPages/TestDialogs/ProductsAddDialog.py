#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPages.PageActions.NotificationVerifier import NotificationVerifier


class ProductsAddDialog(NotificationVerifier):
    def __init__(self, webdriver):
        super(ProductsAddDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def add_entry_and_save(self, name, display, sage, default_cut):
        self.wait()

        self.name.send_keys(name)
        self.display.send_keys(display)
        self.sage.send_keys(sage)
        self.default_cut.select_input(default_cut)

        self.save_button.click()

    @property
    def name(self):
        return EditField(self.webdriver, index=0)

    @property
    def display(self):
        return EditField(self.webdriver, index=1)

    @property
    def sage(self):
        return EditField(self.webdriver, index=2)

    @property
    def default_cut(self):
        return Dropdown(self.webdriver)

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-success")
