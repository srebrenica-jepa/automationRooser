#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.AccountSettingsPage import AccountSettingsPage
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.Dropdown import Dropdown, DropdownSelect


class ChangeMyPasswordPage(AccountSettingsPage):
    def navigate(self):
        super(AccountDetailsPage, self).navigate()
        self.wait()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.tab-pane.active'))
        WebDriverWait(self.webdriver, 20).until(header)

    @property
    def current_password(self):
        return EditField(self.webdriver, index=3)

    @property
    def new_password(self):
        return EditField(self.webdriver, index=4)

    @property
    def new_password_confirmation(self):
        return EditField(self.webdriver, index=5)
