#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Common.Utilities.Logging import PrintMessage
from TestExecute.TestContext import Test_Context
from TestPages.BasePage import BasePage
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField


class LoginPageForm(BasePage):
    def navigate(self):
        config = Test_Context.run_config.load('Deployment_Values')
        automation_ip = config['automation']['IP_ADDRESS']
        PrintMessage('Logging at address: {0}'.format(automation_ip))
        self.webdriver.get('https://{0}'.format(automation_ip))

    def wait(self):
        form_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div#app'))
        WebDriverWait(self.webdriver, 20).until(form_present)

    def perform_login(self, user_name, password):
        self.load()
        self.username.send_keys(user_name)
        self.password.send_keys(password)
        self.login_button.click()
        PrintMessage('User {0} logged in.'.format(user_name))

    @property
    def username(self):
        return EditField(self.webdriver, index=0)

    @property
    def password(self):
        return EditField(self.webdriver, index=1)

    @property
    def login_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-primary')


