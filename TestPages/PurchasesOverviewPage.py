#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.CTAButton import CTAButton
from TestPageObjects.Table.BaseTable import BaseTable
from TestPages.TestPageObjects.Table.TableRow import TableType


class PurchasesOverviewPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_purchases_button.click()
        self.wait()
        self.dashboard_object.main_menu_purchases_overview_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 40).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'main'))
        WebDriverWait(self.webdriver, 40).until(analysis_page)

    @property
    def title_by_office(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value=".row > div:nth-child(1) > div > div:nth-child(1) > strong").get_html()

    @property
    def title_by_species(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value=".row > div:nth-child(2) > div > div:nth-child(1) > strong").get_html()
