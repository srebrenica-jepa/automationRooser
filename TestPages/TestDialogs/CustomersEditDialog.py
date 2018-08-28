#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPages.TestPageObjects.CheckBox import CheckBox
from TestPages.PageEnums import Currency, Weight


class CustomersEditDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_and_confirm(self, name, sage_code, display=None, transport=None,
    currency=Currency.Pound, weight=Weight.Kg, hygiene=False):
        self.wait()

        self.name.clear()
        self.name.send_keys(name)
        self.sage.clear()
        self.sage.send_keys(sage_code)

        if display:
            self.display.send_keys(display)
        if transport:
            self.transport.select_input(transport)
        if currency == Currency.Euro or currency == Currency.Dollar:
            self.currency.select_input(currency)
        if weight == Weight.St:
            self.stone.click()
        else:
            self.kg.click()
        if hygiene:
            self.hygiene.click()

        self.save_button.click()

    @property
    def name(self):
        return EditField(self.webdriver)

    @property
    def display(self):
        return EditField(self.webdriver, index=1)

    @property
    def sage(self):
        return EditField(self.webdriver, index=2)

    @property
    def transport(self):
        return Dropdown(self.webdriver)

    @property
    def currency(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def kg(self):
        return CheckBox(self.webdriver, By.CSS_SELECTOR, '.form-check-input', index=0)

    @property
    def stone(self):
        return CheckBox(self.webdriver, By.CSS_SELECTOR, '.form-check-input', index=1)

    @property
    def hygiene(self):
        return CheckBox(self.webdriver, By.CSS_SELECTOR, '.form-check-input', index=2)

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-success")
