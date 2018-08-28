#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.TestDialogs.CategoriesEditDialog import CategoriesEditDialog
from TestPages.TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestPages.TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.InvariableField import InvariableField


class CategoriesCheckDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'container-fluid'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_entry(self, name, species=None, product=None, cut=None, whole=None, headless=None, on_on=None,
                   on_off=None, off_on=None, off_off=None, j_cut_on=None, j_cut_off=None, butterfly=None, off_v=None):
        self.wait()
        self.edit_button.click()
        edit_dialog = CategoriesEditDialog(self.webdriver)
        edit_dialog.wait()
        edit_dialog.edit_and_confirm(name, species, product, cut, whole, headless, on_on, on_off, off_on, off_off, j_cut_on, j_cut_off, butterfly, off_v)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Category edited.')

    def remove_entry(self, name):
        self.wait()
        self.delete_button.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Category deleted.')

    @property
    def category_name(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'h3').get_html()

    @property
    def edit_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-primary")

    @property
    def delete_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")

