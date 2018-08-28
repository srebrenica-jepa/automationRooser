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


class SalesOverviewPage(BaseDashboardPage):
    def navigate(self):
        self.wait_for_page()
        self.dashboard_object.main_menu_sales_button.click()
        self.wait_for_page()
        self.dashboard_object.main_menu_sales_overview_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 40).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'main'))
        WebDriverWait(self.webdriver, 40).until(analysis_page)

    @property
    def title_average(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value="div.row:nth-child(1) > div > div > .card-header > strong").get_html()

    @property
    def title_hygiene(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value="div.row:nth-child(2) > div:nth-child(1) > div > .card-header > strong").get_html()

    @property
    def title_fish(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value="div.row:nth-child(2) > div:nth-child(2) > div > .card-header > strong").get_html()

    @property
    def title_invoice(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value="div.row:nth-child(2) > div:nth-child(3) > div > .card-header > strong").get_html()

    @property
    def title_summary(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value="div.row:nth-child(2) > div:nth-child(4) > div > .card-header > strong").get_html()
