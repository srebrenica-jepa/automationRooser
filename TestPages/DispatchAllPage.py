#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.CTAButton import CTAButton
from TestPageObjects.Table.BaseTable import BaseTable
from TestPages.TestPageObjects.Table.TableRow import TableType


class DispatchAllPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_dispatch_button.click()
        self.dashboard_object.main_menu_dispatch_all_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 40).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-fluid'))
        WebDriverWait(self.webdriver, 40).until(analysis_page)

    @property
    def table(self):
        return BaseTable(self.webdriver, table_type=TableType.without_details_type)

    @property
    def title(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value="h2").get_html()

    @property
    def refresh_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-primary')

    @property
    def refresh_button_text(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value='.pull-right.btn').get_text_without_react()

    @property
    def filter_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-primary', index=1)
