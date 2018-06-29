#!/usr/bin/env python
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.BasePage import BasePage

from TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.InvariableField import InvariableField


class SessionExpiredPage(BasePage):
    def wait(self):
        session_expired = EC.presence_of_element_located((By.CLASS_NAME, 'log-back'))
        WebDriverWait(self.webdriver, 10).until(session_expired)

    @property
    def information_container(self):
        return InvariableField(self.webdriver, By.CLASS_NAME, "information-container").get_html()

    @property
    def log_back_in(self):
        return CTAButton(self.webdriver, By.CLASS_NAME, "log-back")

    @property
    def copyright(self):
        return InvariableField(self.webdriver, By.CLASS_NAME, "copyright-information").get_html()
