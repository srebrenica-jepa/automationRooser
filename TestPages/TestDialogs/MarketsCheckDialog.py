#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.TestDialogs.MarketsEditDialog import MarketsEditDialog
from TestPages.TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestPages.TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.InvariableField import InvariableField


class MarketsCheckDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'container-fluid'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_entry(self, name, number_of_doors, delivery_time=None, market_cost=None):
        self.wait()
        self.edit_button.click()
        edit_dialog = MarketsEditDialog(self.webdriver)
        edit_dialog.edit_and_confirm(name, number_of_doors, delivery_time, market_cost)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Market edited.')

    def remove_entry(self, name):
        self.wait()
        self.delete_button.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Market deleted.')

    @property
    def market_name(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'h3').get_html()

    @property
    def edit_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-primary")

    @property
    def delete_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")
