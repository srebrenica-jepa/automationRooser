#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestPageObjects.RadioButtons import RadioButton
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPageObjects.EditField import EditField
from TestPageObjects.CTAButton import CTAButton
from TestPages.PageActions.NotificationVerifier import NotificationVerifier
from TestPages.PageEnums import State


class CreateTenantPage(NotificationVerifier):
    def __init__(self, webdriver):
        super(CreateTenantPage, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        create_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-tenant-detail'))
        WebDriverWait(self.webdriver, 20).until(create_page)

    def set_status(self, status):
        if status == State.Enabled:
            self.status_enable.click()
        else:
            self.status_disable.click()

    def add_entry_and_save(self, tenant_name, description, service_level, name, email, status=True, phone=None,
                           address=None, country=None):
        self.tenant_name.send_keys(tenant_name)
        self.description.send_keys(description)
        self.service_level.select_input(service_level)
        self.set_status(status)
        self.name.send_keys(name)
        self.email.send_keys(email)
        if phone:
            self.phone.send_keys(phone)
        if address:
            self.address.send_keys(address)
        self.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        if country:
            self.country.select_input(country)

        self.save_button.click()

    @property
    def tenant_name(self):
        return EditField(self.webdriver, index=1)

    @property
    def description(self):
        return EditField(self.webdriver, value="textarea.form-control")

    @property
    def service_level(self):
        return Dropdown(self.webdriver, index=3)

    @property
    def status_enable(self):
        return RadioButton(self.webdriver)

    @property
    def status_disable(self):
        return RadioButton(self.webdriver, index=1)

    @property
    def name(self):
        return EditField(self.webdriver, index=2)

    @property
    def email(self):
        return EditField(self.webdriver, index=3)

    @property
    def phone(self):
        return EditField(self.webdriver, index=4)

    @property
    def address(self):
        return EditField(self.webdriver, index=5)

    @property
    def country(self):
        return Dropdown(self.webdriver, index=4)

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-blue')

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-simple')




