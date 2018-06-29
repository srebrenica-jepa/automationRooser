#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.SystemPage import SystemPage
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPages.TestPageObjects.CheckBox import CheckBox
from TestPages.TestPageObjects.EditField import EditField
from TestPages.PageActions.NotificationVerifier import NotificationVerifier
from TestPages.PageEnums import State


class SystemPasswordPage(SystemPage, NotificationVerifier):
    def wait(self):
        system_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rc-tabs'))
        WebDriverWait(self.webdriver, 20).until(system_page)

    def set_options(self, password_expiration=None, password_expiration_warning_period=None, password_change_grace_period=None,
                    onscreen_notification=State.Disabled, email_notification=State.Disabled, send_password_email_notifications=None):
        if password_expiration:
            self.passwords_expire_after.select_input(password_expiration)
        if password_expiration_warning_period:
            self.password_expiration_warning_period.select_input(password_expiration_warning_period)
        if password_change_grace_period:
            self.password_change_grace_period.select_input(password_change_grace_period)
        if onscreen_notification == State.Enabled:
            self.onscreen_password_notifications.click()
        if email_notification == State.Enabled:
            self.email_password_notifications.click()
        if send_password_email_notifications:
            self.send_password_email_notifications_at.send_keys(send_password_email_notifications)

        self.save_button.click()

    @property
    def passwords_expire_after(self):
        return Dropdown(self.webdriver, index=0)

    @property
    def password_expiration_warning_period(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def password_change_grace_period(self):
        return Dropdown(self.webdriver, index=2)

    @property
    def onscreen_password_notifications(self):
        return CheckBox(self.webdriver, By.CSS_SELECTOR, '.form-checkbox-wrapper', index=0)

    @property
    def email_password_notifications(self):
        return CheckBox(self.webdriver, By.CSS_SELECTOR, '.form-checkbox-wrapper', index=1)

    @property
    def send_password_email_notifications_at(self):
        return EditField(self.webdriver)

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn.btn-primary')

    @property
    def title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.corero-page-title').get_html()

    @property
    def subtitle(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div.rc-tabs-tabpane > div > div > div').get_html()

    @property
    def passwords_expire_after_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'form > div:nth-of-type(1) > div > label').get_html()

    @property
    def password_expiration_warning_period_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'form > div:nth-of-type(2) > div > label').get_html()

    @property
    def password_change_grace_period_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'form > div:nth-of-type(3) > div > label').get_html()

    @property
    def onscreen_password_notifications_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'form > div:nth-of-type(4) > label').get_html()

    @property
    def email_password_notifications_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'form > div:nth-of-type(5) > label').get_html()

    @property
    def send_password_email_notifications_at_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'form > div:nth-of-type(6) > div > label').get_html()


