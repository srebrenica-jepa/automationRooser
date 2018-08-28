#!/usr/bin/env python
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Common.Utilities.Logging import PrintMessage

from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.BasePage import BasePage


class LogBackInPage(BasePage):
    def wait(self):
        login_form_present = EC.presence_of_all_elements_located((By.CLASS_NAME, 'login-button'))
        WebDriverWait(self.webdriver, 10).until(login_form_present)

    def login(self, user_name, password):
        time.sleep(50)
        self.username.send_keys(user_name)
        self.password.send_keys(password)
        self.login_button.click()
        PrintMessage('User {0} logged in.'.format(user_name))

    @property
    def login_information(self):
        return InvariableField(self.webdriver, By.CLASS_NAME, "information-container").get_html()

    @property
    def username(self):
        return EditField(self.webdriver, by_type=By.NAME, value="username")

    @property
    def password(self):
        return EditField(self.webdriver, by_type=By.NAME, value="password")

    @property
    def login_button(self):
        return CTAButton(self.webdriver, By.CLASS_NAME, "login-button")

    @property
    def copyright(self):
        return InvariableField(self.webdriver, By.CLASS_NAME, "copyright-information").get_html()
