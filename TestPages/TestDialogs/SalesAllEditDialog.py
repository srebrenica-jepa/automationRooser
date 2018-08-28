#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField


class SalesAllEditDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_and_confirm(self, customer, transport, product, cut, quantity, weight, price):
        self.wait()

        self.customer.select_input_enter(customer)
        self.new_sale.click()

        self.wait()
        self.transport.select_input_enter(transport)
        self.product.select_input_enter(product)
        self.new_sale.click()

        self.cut.select_input_enter(cut)
        self.quantity.send_keys(quantity)
        self.weight.send_keys(weight)
        self.price.send_keys(price)

        self.save_button.click()

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
    def save_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn-success', index=1)