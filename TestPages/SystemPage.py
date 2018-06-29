#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestPages.TestPageObjects.CTAButton import CTAButton


class SystemPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_system_button.click()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.page-default-subheader'))
        WebDriverWait(self.webdriver, 40).until(header)

    @property
    def users_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']")

    @property
    def ldap_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=1)

    @property
    def audit_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=2)

    @property
    def policy_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=3)

    @property
    def reporting_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=4)

    @property
    def licensing_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=5)

    @property
    def logo_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=6)

    @property
    def password_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[role='tab']", index=7)
