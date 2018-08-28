#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.PageActions.NotificationVerifier import NotificationVerifier


class PurchasesAddDialog(NotificationVerifier):
    def __init__(self, webdriver):
        super(PurchasesAddDialog, self).__init__(webdriver)
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'container-fluid'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def add_entry_and_save(self, date, no_boxes, kg, cost, species, market, market_door, boat):
        self.wait()

        self.date.send_keys(date)
        self.no_boxes.send_keys(no_boxes)
        self.kg.send_keys(kg)
        self.cost.send_keys(cost)
        self.species.select_input(species)
        self.market.select_input(market)
        self.market_door.send_keys(market_door)
        self.boat.select_input(boat)
        self.save_button.click()

    @property
    def date(self):
        return EditField(self.webdriver)

    @property
    def no_boxes(self):
        return EditField(self.webdriver, index=1)

    @property
    def kg(self):
        return EditField(self.webdriver, index=2)

    @property
    def cost(self):
        return EditField(self.webdriver, index=3)

    @property
    def species(self):
        return Dropdown(self.webdriver)

    @property
    def market(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def market_door(self):
        return EditField(self.webdriver, index=4)

    @property
    def boat(self):
        return Dropdown(self.webdriver, index=2)

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-default")

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-success")

    @property
    def error(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, "div>ul>li:nth-child(1)").get_html()
