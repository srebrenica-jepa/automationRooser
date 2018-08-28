#!/usr/bin/env python
from selenium.webdriver.common.by import By

from TestPages.TestPageObjects.Table.TableRowField import TableRowField
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.Dropdown import Dropdown


class TableType(object):
    without_details_type = 1
    with_details_type = 2
    other = 3


class TableRow(object):
    def __init__(self, row_element, row_headers, table_type=TableType.without_details_type):
        self._row_element = row_element
        self._row_headers = row_headers
        self._table_type = table_type

    def __getitem__(self, column_name):
        index = self._row_headers.index(column_name)
        return self.fields[index].text

    def __len__(self):
        return len(self.fields)

    def get_raw_row_fields(self):
        if self._table_type == TableType.without_details_type or self._table_type == TableType.with_details_type:
            return self._row_element.find_elements_by_css_selector('td')
        elif self._table_type == TableType.other:
            return self._row_element.find_elements_by_css_selector('.box-tenant-item > div')
        else:
            return None

    @property
    def fields(self):
        row_fields = self.get_raw_row_fields()
        return [TableRowField(k) for k in row_fields]


class TableRowWithoutDetails(TableRow):
    @property
    def edit_row_item(self):
        return CTAButton(self._row_element, By.CSS_SELECTOR, ".btn-secondary.btn-sm")

    @property
    def delete_row_item(self):
        return CTAButton(self._row_element, By.CSS_SELECTOR, ".btn-danger.btn-sm")


class TableRowWithDetails(TableRowWithoutDetails):
    @property
    def details_row_item(self):
        return Dropdown(self._row_element, By.CSS_SELECTOR, ".btn-primary.btn-sm")
