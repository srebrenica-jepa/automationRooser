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
from TestPageObjects.Dropdown import Dropdown
from TestPageObjects.EditField import EditField
from TestPageObjects.Table.BaseTable import BaseTable
from TestPages.TestPageObjects.Table.TableRow import TableType


class StocksAllPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_stocks_button.click()
        self.wait()
        self.dashboard_object.main_menu_stocks_all_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 40).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-fluid'))
        WebDriverWait(self.webdriver, 40).until(analysis_page)

    def add_entry(self, market, category, cut, number_of_boxes, box_weight, cost_per_kg):
        self.wait()
        self.market.select_input(market)
        self.category.select_input(category)
        self.cut.select_input(cut)
        self.number_of_boxes.send_keys(number_of_boxes)
        self.box_weight.send_keys(box_weight)
        self.cost_per_kg.send_keys(cost_per_kg)
        self.add_button.click()
        PrintMessage('Filet created.')

    def remove_entry(self, name):
        row = self.table.get_row_for_field_value(TableHeaders.Name, name)
        self.delete_row(row)

    def delete_row(self, row):
        self.wait()
        self.wait_for_page()
        row.delete_row_item.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Filet deleted.')

    @property
    def table(self):
        return BaseTable(self.webdriver, table_type=TableType.without_details_type)

    @property
    def title(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value="h1").get_html()

    @property
    def subtitle(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value="h3").get_html()

    @property
    def market(self):
        return Dropdown(self.webdriver)

    @property
    def category(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def cut(self):
        return Dropdown(self.webdriver, index=2)

    @property
    def number_of_boxes(self):
        return EditField(self.webdriver)

    @property
    def box_weight(self):
        return EditField(self.webdriver, index=1)

    @property
    def cost_per_kg(self):
        return EditField(self.webdriver, index=2)

    @property
    def add_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-success')

    @property
    def delete_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")