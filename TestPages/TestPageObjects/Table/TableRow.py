#!/usr/bin/env python
from selenium.webdriver.common.by import By

from TestPages.TestPageObjects.Table.TableRowField import TableRowField
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.Dropdown import Dropdown


class TableType(object):
    button_action_type = 1
    dropdown_action_type = 2
    status_action_type = 3


class TableRow(object):
    def __init__(self, row_element, row_headers, table_type=TableType.button_action_type):
        self._row_element = row_element
        self._row_headers = row_headers
        self._table_type = table_type

    def __getitem__(self, column_name):
        index = self._row_headers.index(column_name)
        return self.fields[index].text

    def __len__(self):
        return len(self.fields)

    def get_raw_row_fields(self):
        if self._table_type == TableType.button_action_type:
            return self._row_element.find_elements_by_css_selector('td > div')
        elif self._table_type == TableType.status_action_type:
            return self._row_element.find_elements_by_css_selector('.box-tenant-item > div')
        else:
            return None

    @property
    def fields(self):
        row_fields = self.get_raw_row_fields()
        return [TableRowField(k) for k in row_fields]


class TableRowButtonAction(TableRow):
    @property
    def edit_row_item(self):
        return CTAButton(self._row_element, By.CLASS_NAME, "icon-edit-small")

    @property
    def delete_row_item(self):
        return CTAButton(self._row_element, By.CLASS_NAME, "icon-delete_icon")

    @property
    def lock_row_item(self):
        return CTAButton(self._row_element, By.CLASS_NAME, "cicon-lock")

    @property
    def stop_row_item(self):
        return CTAButton(self._row_element, By.CLASS_NAME, "icon-stop_icon")

    @property
    def start_row_item(self):
        return CTAButton(self._row_element, By.CLASS_NAME, "icon-start_icon")


class TableRowDropdownAction(TableRow):
    @property
    def actions(self):
        return Dropdown(self._row_element)


class TableRowStatusAction(TableRow):
    @property
    def status_icon(self):
        return CTAButton(self._row_element, By.CSS_SELECTOR, ".green-default")

