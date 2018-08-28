#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.Dropdown import DropdownMenu


class UsersEditDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_and_confirm(self, first_name, last_name, email, password, role=None, market=None):
        self.wait()

        self.first_name.send_keys(first_name)
        self.last_name.send_keys(last_name)
        self.email.send_keys(email)
        self.password.send_keys(password)
        self.role.select_input(role)
        if market:
            self.market.select_input(market)

        self.save_button.click()

    @property
    def first_name(self):
        return EditField(self.webdriver, index=0)

    @property
    def last_name(self):
        return EditField(self.webdriver, index=1)

    @property
    def email(self):
        return EditField(self.webdriver, index=2)

    @property
    def password(self):
        return EditField(self.webdriver, index=3)

    @property
    def role(self):
        return DropdownMenu(self.webdriver)

    @property
    def market(self):
        return DropdownMenu(self.webdriver, index=1)

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-success")
