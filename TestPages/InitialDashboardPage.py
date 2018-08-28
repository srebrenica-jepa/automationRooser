#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.Dropdown import Dropdown, DropdownSelect


class InitialDashboardPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_dashboard_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 20).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-fluid'))
        WebDriverWait(self.webdriver, 20).until(analysis_page)

    @property
    def purchases_summary(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div:nth-child(1) > div > div:nth-child(1) > strong').get_html()

    @property
    def sales_summary(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div:nth-child(2) > div > div:nth-child(1) > strong').get_html()

