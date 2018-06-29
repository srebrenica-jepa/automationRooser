#!/usr/bin/env python
from selenium.webdriver.common.by import By

from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind
from TestPages.TestPageObjects.Table.TableRow import TableRowButtonAction
from TestPages.TestPageObjects.Table.TableRow import TableRowDropdownAction
from TestPages.TestPageObjects.Table.TableRow import TableRowStatusAction
from TestPages.TestPageObjects.Table.TableRow import TableType


class BaseTable(object):
    def __init__(self, webdriver, table_type=TableType.button_action_type, index=0):
        """

        :param webdriver:
        :param table_type:
        :param index: in case of multiple tables on the page, index indicates specific table
        """
        self.web_driver_find = WebdriverFind(webdriver)
        self.table_index = index
        self.table_type = table_type

    def get_raw_rows(self):
        if self.table_type == TableType.status_action_type:
            return self.table_element.find_elements_by_css_selector('.box-tenant-item')
        else:
            return self.table_element.find_elements_by_css_selector('tr')

    @property
    def table_element(self):
        if self.table_type == TableType.status_action_type:
            return self.web_driver_find.find_all(By.CSS_SELECTOR, '.container-list')[self.table_index]
        else:
            return self.web_driver_find.find_all(By.CSS_SELECTOR, '.wrapper-table')[self.table_index]

    @property
    def row_count(self):
        return len(self.rows)

    @property
    def column_count(self):
        return 0

    @property
    def rows(self):
        """
        Assume first row of a table is header
        Assumes header element is a single item with text: Column1\nColumn2\nColumn3
        :return:
        """
        all_rows = self.get_raw_rows()

        if self.table_type == TableType.status_action_type and len(all_rows) > 0:
            row_headers = all_rows[0].text.split('\n')[0].split()
        else:
            if len(all_rows) > 0:
                row_headers_string = all_rows[0].text.split('\n')[0]
                row_headers = self.split_uppercase(row_headers_string)
            else:
                row_headers = []

        #if len(all_rows) > 0:
        #    row_headers = all_rows[0].text.split('\n')
        #else:
        #    row_headers = None

        if self.table_type == TableType.button_action_type:
                return [TableRowButtonAction(row, row_headers, table_type=TableType.button_action_type) for row in
                        all_rows[1:]]
        elif self.table_type == TableType.dropdown_action_type:
                return [TableRowDropdownAction(row, row_headers, table_type=TableType.dropdown_action_type) for row in
                        all_rows[1:]]
        elif self.table_type == TableType.status_action_type:
            return [TableRowStatusAction(row, row_headers, table_type=TableType.status_action_type) for row in
                    all_rows[1:]]
        else:
            return []

    def get_row_for_field_value(self, column_name, field_value):
        for row in self.rows:
            if row[column_name] == field_value:
                return row

        return None

    def split_uppercase(self, str):
        """
        Splits headers that are not separated by newline or space.
        Assumes header element is a single item with text: Column1Column2Column3
        :return: a list of all the column names
        """
        i = 0
        j = 0
        list_of_headers = []

        for c in str:
            if c.isupper() and (str[j-1].islower() or str[j-1] == ')'):
                current_header = str[i:j]
                list_of_headers.append(current_header)
                i = j
            j += 1

        if j == len(str):
            last_header = str[i:j]
            list_of_headers.append(last_header)
        list_of_headers = filter(None, list_of_headers)
        return list_of_headers


