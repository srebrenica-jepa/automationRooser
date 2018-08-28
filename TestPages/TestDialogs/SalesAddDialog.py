#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPages.PageActions.NotificationVerifier import NotificationVerifier


class SalesAddDialog(NotificationVerifier):
    def __init__(self, webdriver):
        super(SalesAddDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'h2'))
        WebDriverWait(self.webdriver, 40).until(add_dialog)

    def add_entry_and_save(self, cut, quantity, weight, price):
        self.wait()

        self.cut.select_input_enter(cut)
        self.quantity.send_keys(quantity)
        self.weight.send_keys(weight)
        self.price.send_keys(price)

        self.add_button.click()

    @property
    def cut(self):
        return Dropdown(self.webdriver, index=2)


    @property
    def quantity(self):
        return EditField(self.webdriver, index=3)

    @property
    def weight(self):
        return EditField(self.webdriver, index=4)

    @property
    def price(self):
        return EditField(self.webdriver, index=5)

    @property
    def add_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-success')