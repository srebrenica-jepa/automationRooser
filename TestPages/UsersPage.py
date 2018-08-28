#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestDialogs.UsersEditDialog import UsersEditDialog
from TestDialogs.UsersAddDialog import UsersAddDialog
from TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.CTAButton import CTAButton
from PageEnums import HeadersUsers
from TestPageObjects.Table.BaseTable import BaseTable
from TestPages.TestPageObjects.Table.TableRow import TableType


class UsersPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_users_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 40).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-fluid'))
        WebDriverWait(self.webdriver, 40).until(analysis_page)

    def add_entry(self, first_name, last_name, email, password, role=None, market=None):
        self.wait()
        self.add_button.click()
        add_dialog = UsersAddDialog(self.webdriver)
        if market==None:
            add_dialog.add_entry_and_save(first_name, last_name, email, password, role)
        else:
            add_dialog.add_entry_and_save(first_name, last_name, email, password, role, market)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('User created.')

    def edit_entry(self, row, first_name, last_name, email, password, role=None, market=None):
        self.wait()
        self.wait_for_page()
        row.edit_row_item.click()
        edit_dialog = UsersEditDialog(self.webdriver)
        if market==None:
            edit_dialog.edit_and_confirm(first_name, last_name, email, password, role)
        else:
            edit_dialog.edit_and_confirm(first_name, last_name, email, password, role, market)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('User edited.')

    def remove_entry(self, name):
        row = self.table.get_row_for_field_value(HeadersUsers.FirstName, name)
        self.delete_row(row)

    def delete_row(self, row):
        self.wait()
        self.wait_for_page()
        row.delete_row_item.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('User deleted.')

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
    def add_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-success')
