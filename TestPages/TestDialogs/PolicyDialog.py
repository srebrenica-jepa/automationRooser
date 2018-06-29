#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.PageActions.NotificationVerifier import NotificationVerifier


class PolicyDialog(NotificationVerifier):
    def __init__(self, webdriver):
        super(PolicyDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'modal-header'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    @property
    def general_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=9)

    @property
    def service_level_alerts_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=10)

    @property
    def attack_status_alerts_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=11)


