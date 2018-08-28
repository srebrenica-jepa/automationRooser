#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.CTAButton import CTAButton


class AccountSettingsPage(BaseDashboardPage):
    def navigate(self):
        self.dashboard_object.main_menu_dashboard_button.click()
        self.wait()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.breadcrumb'))
        WebDriverWait(self.webdriver, 20).until(header)

    @property
    def account_details_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, 'li>.nav-link', index=21)

    @property
    def change_my_password_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, 'li>.nav-link', index=22)
    
    
    
    
    
    

















