#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage


from TestPages.TestDialogs.TransportsEditDialog import TransportsEditDialog
from TestPages.TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestPages.TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestPages.PageEnums import State
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.PageActions.NotificationVerifier import NotificationVerifier
from TestPages.PageEnums import CheckOneBox


class TransportsCheckDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'container-fluid'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_entry(self, name, weight=None, shipping=CheckOneBox.no):
        self.wait()
        self.edit_button.click()
        edit_dialog = TransportsEditDialog(self.webdriver)
        edit_dialog.edit_and_confirm(name, weight, shipping)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Transport edited.')

    def remove_entry(self, name):
        self.wait()
        self.delete_button.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Transport deleted.')

    @property
    def transport_name(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'h3').get_html()

    @property
    def delivers(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'hr').get_html()

    @property
    def edit_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-primary")

    @property
    def delete_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")
