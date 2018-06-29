#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.PageActions.NotificationVerifier import NotificationVerifier


class ReportDialog(NotificationVerifier):
    def __init__(self, webdriver):
        super(ReportDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.modal-content'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    @property
    def report_setup_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=11)

    @property
    def mail_setup_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=12)



