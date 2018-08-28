#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.Dropdown import Dropdown


class BoatsEditDialog(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def edit_and_confirm(self, name, office):
        self.wait()
        self.name.clear()
        self.name.send_keys(name)
        self.office.select_input(office)
        self.save_button.click()

    @property
    def name(self):
        return EditField(self.webdriver)

    @property
    def office(self):
        return Dropdown(self.webdriver)

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-success")
