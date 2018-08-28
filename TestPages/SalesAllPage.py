#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestDialogs.SalesAllAddDialog import SalesAllAddDialog
from TestDialogs.SalesAllEditDialog import SalesAllEditDialog
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.CTAButton import CTAButton
from TestPageObjects.Dropdown import Dropdown
from TestPageObjects.Table.BaseTable import BaseTable
from TestPages.TestPageObjects.Table.TableRow import TableType
from TestPages.PageEnums import HeadersSales


class SalesAllPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_sales_button.click()
        self.wait()
        self.dashboard_object.main_menu_sales_all_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 40).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-fluid'))
        WebDriverWait(self.webdriver, 40).until(analysis_page)

    def add_entry(self, customer, transport, product, cut, quantity, weight, price):
        self.wait()
        self.add_button.click()
        add_dialog = SalesAllAddDialog(self.webdriver)
        add_dialog.add_entry_and_save(customer, transport, product, cut, quantity, weight, price)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Sale created.')

    def edit_entry(self, row, customer, transport, product, cut, quantity, weight, price):
        self.wait_for_page()
        row.edit_row_item.click()
        edit_dialog = SalesAllEditDialog(self.webdriver)
        edit_dialog.edit_and_confirm(customer, transport, product, cut, quantity, weight, price)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Customer edited.')

    def remove_entry(self, name):
        self.wait_for_page()
        row = self.table.get_row_for_field_value(HeadersSales.Customer, name)
        self.delete_row(row)

    def delete_row(self, row):
        self.wait_for_page()
        row.delete_row_item.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Customer deleted.')

    @property
    def table(self):
        return BaseTable(self.webdriver, table_type=TableType.without_details_type)

    @property
    def title(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value=".card-body > h2").get_html()

    @property
    def subtitle(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value=".card-body > p").get_text_without_react()

    @property
    def customer(self):
        return Dropdown(self.webdriver)

    @property
    def product(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def empty_text(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value=".react-bs-table-no-data").get_html()

    @property
    def add_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-success')

