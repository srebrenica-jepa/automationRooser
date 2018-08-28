#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField


class MarketsEditDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_and_confirm(self, name, number_of_doors, delivery_time=None, market_cost=None):
        self.wait()

        self.name.send_keys(name)
        self.number_of_doors.send_keys(number_of_doors)
        if delivery_time:
            self.delivery_time.send_keys(delivery_time)

        if market_cost:
            self.market_cost.send_keys(market_cost)

        self.save_button.click()

    @property
    def name(self):
        return EditField(self.webdriver, index=0)

    @property
    def number_of_doors(self):
        return EditField(self.webdriver, index=1)

    @property
    def delivery_time(self):
        return EditField(self.webdriver, index=2)

    @property
    def market_cost(self):
        return EditField(self.webdriver, index=3)

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-success")
