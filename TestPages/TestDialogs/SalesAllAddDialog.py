#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestDialogs.SalesAddDialog import SalesAddDialog
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.PageActions.NotificationVerifier import NotificationVerifier


class SalesAllAddDialog(NotificationVerifier):
    def __init__(self, webdriver):
        super(SalesAllAddDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h2'))
        WebDriverWait(self.webdriver, 40).until(add_dialog)

    def add_entry_and_save(self, customer, transport,  product, cut, quantity, weight, price):
        self.wait()

        self.customer.select_input_enter(customer)
        self.new_sale.click()

        self.wait()
        self.transport.select_input_enter(transport)
        self.product.select_input_enter(product)
        self.new_sale.click()

        self.add_button.click()
        add_dialog= SalesAddDialog(self.webdriver)
        add_dialog.add_entry_and_save(cut, quantity, weight, price)

    @property
    def customer(self):
        return Dropdown(self.webdriver)

    @property
    def new_sale(self):
        return InvariableField(self.webdriver, by_type=By.CSS_SELECTOR, value='h2')

    @property
    def transport(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def product(self):
        return Dropdown(self.webdriver, index=2)

    @property
    def add_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-secondary', index=1)


