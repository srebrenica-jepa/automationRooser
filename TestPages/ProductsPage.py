#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestDialogs.ProductsEditDialog import ProductsEditDialog
from TestDialogs.ProductsAddDialog import ProductsAddDialog
from TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.CTAButton import CTAButton
from PageEnums import HeadersProducts
from TestPageObjects.Table.BaseTable import BaseTable
from TestPages.TestPageObjects.Table.TableRow import TableType


class ProductsPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_products_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 40).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-fluid'))
        WebDriverWait(self.webdriver, 40).until(analysis_page)

    def add_entry(self, name, display, sage, default_cut):
        self.wait()
        self.add_button.click()
        add_dialog = ProductsAddDialog(self.webdriver)
        add_dialog.add_entry_and_save(name, display, sage, default_cut)
        self.wait_for_page()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Product created.')

    def edit_entry(self, row, name, display, sage, default_cut):
        self.wait()
        row.edit_row_item.click()
        edit_dialog = ProductsEditDialog(self.webdriver)
        edit_dialog.edit_and_confirm(name, display, sage, default_cut)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Product edited.')

    def remove_entry(self, name):
        row = self.table.get_row_for_field_value(HeadersProducts.Name, name)
        self.delete_row(row)

    def delete_row(self, row):
        self.wait()
        row.delete_row_item.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Product deleted.')

    @property
    def table(self):
        return BaseTable(self.webdriver, table_type=TableType.with_details_type)

    @property
    def title(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value=".card-body > h2").get_html()

    @property
    def subtitle(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value=".card-body > p").get_html()

    @property
    def empty_text(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value=".react-bs-table-no-data").get_html()

    @property
    def add_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-success')
