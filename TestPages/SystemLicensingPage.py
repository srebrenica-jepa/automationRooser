#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.SystemPage import SystemPage
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.PageActions.NotificationVerifier import NotificationVerifier


class SystemLicensingPage(SystemPage, NotificationVerifier):
    def wait(self):
        system_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rc-tabs'))
        WebDriverWait(self.webdriver, 20).until(system_page)

    @property
    def add_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn.btn-primary')

    @property
    def confirm_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn.btn-primary')

    @property
    def license_key(self):
        return EditField(self.webdriver)

    @property
    def title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.corero-page-title')

    @property
    def subtitle(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > h3')

    @property
    def current_license_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div.licensing > div:nth-child(2) > div')


