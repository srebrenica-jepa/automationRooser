#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.TestDialogs.SalesAllEditDialog import SalesAllEditDialog
from TestPages.TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestPages.TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.InvariableField import InvariableField


class SalesAllCheckDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'container-fluid'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_entry(self, customer, transport, product, cut, quantity, weight, price):
        self.wait()
        self.edit_button.click()
        edit_dialog = SalesAllEditDialog(self.webdriver)
        edit_dialog.wait()
        edit_dialog.edit_and_confirm(customer, transport, product, cut, quantity, weight, price)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Sale edited.')

    def remove_entry(self, name):
        self.wait()
        self.delete_button.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Sale deleted.')

    @property
    def customer_name(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, "div> div > div:nth-child(1) > div:nth-child(1) > span").get_html()

    @property
    def edit_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-primary")

    @property
    def delete_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")

