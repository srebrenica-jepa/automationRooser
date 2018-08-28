#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPages.PageActions.NotificationVerifier import NotificationVerifier


class CategoriesAddDialog(NotificationVerifier):
    def __init__(self, webdriver):
        super(CategoriesAddDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'card-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def add_entry_and_save(self, name, species=None, product=None, cut=None, whole=None, headless=None, on_on=None,
                           on_off=None, off_on=None, off_off=None, j_cut_on=None, j_cut_off=None, butterfly=None, off_v=None):
        self.wait()

        self.name.send_keys(name)

        if species:
            self.species.select_input_enter(species)

        if product:
            self.product.select_input_enter(product)

        if cut:
            self.cut.select_input(cut)

        if whole:
            self.whole.send_keys(whole)

        if headless:
            self.headless.send_keys(headless)

        if on_on:
            self.on_on.send_keys(on_on)

        if on_off:
            self.on_off.send_keys(on_off)

        if off_on:
            self.off_on.send_keys(off_on)

        if off_off:
            self.off_off.send_keys(off_off)

        if j_cut_on:
            self.j_cut_on.send_keys(j_cut_on)

        if j_cut_off:
            self.j_cut_off.send_keys(j_cut_off)

        if butterfly:
            self.butterfly.send_keys(butterfly)

        if off_v:
            self.off_v.send_keys(off_v)

        self.save_button.click()

    @property
    def name(self):
        return EditField(self.webdriver, index=0)

    @property
    def species(self):
        return Dropdown(self.webdriver, index=0)


    @property
    def product(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def cut(self):
        return Dropdown(self.webdriver, index=2)

    @property
    def whole(self):
        return EditField(self.webdriver, index=1)

    @property
    def headless(self):
        return EditField(self.webdriver, index=2)

    @property
    def on_on(self):
        return EditField(self.webdriver, index=3)

    @property
    def on_off(self):
        return EditField(self.webdriver, index=4)

    @property
    def off_on(self):
        return EditField(self.webdriver, index=5)

    @property
    def off_off(self):
        return EditField(self.webdriver, index=6)

    @property
    def j_cut_on(self):
        return EditField(self.webdriver, index=7)

    @property
    def j_cut_off(self):
        return EditField(self.webdriver, index=8)

    @property
    def butterfly(self):
        return EditField(self.webdriver, index=9)

    @property
    def off_v(self):
        return EditField(self.webdriver, index=10)

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-danger")

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-success")
