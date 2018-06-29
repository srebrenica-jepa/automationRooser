#!/usr/bin/env python
from selenium.webdriver.common.by import By

from TestPages.TestDialogs.ReportDialog import ReportDialog
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.TestPageObjects.RadioButtons import RadioButton
from TestPages.TestPageObjects.Dropdown import Dropdown
from TestPages.PageEnums import ReportType
from TestPages.TestDialogs.ReportMailSetupAddDialog import Sender
from TestPages.TestDialogs.ReportAddDialog import AddReportTabs
from TestPages.TestDialogs.ReportMailSetupEditDialog import ReportMailSetupEditDialog


class ReportEditDialog(ReportDialog):
    def __init__(self, webdriver):
        super(ReportEditDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def set_type(self, type):
        if type == ReportType.ServiceOverview:
            self.service_overview_enable.click()
        else:
            self.per_tenant_enable.click()

    def edit_and_confirm(self, name, type, timezone, report_setup=AddReportTabs.only_report_setup,
                         subject=None, body=None, send_to=Sender.none):
        self.wait()

        self.name.send_keys(name)
        self.set_type(type)
        self.timezone.select_input(timezone)
        if report_setup == AddReportTabs.only_report_setup:
            self.save_button.click()
        else:
            self.mail_setup_button.click()
            edit_dialog = ReportMailSetupEditDialog(self.webdriver)
            edit_dialog.edit_and_confirm(subject, body, send_to)

    @property
    def name(self):
        return EditField(self.webdriver, index=0)

    @property
    def service_overview_enable(self):
        return RadioButton(self.webdriver)

    @property
    def per_tenant_enable(self):
        return RadioButton(self.webdriver, index=1)

    @property
    def time_period_number(self):
        return EditField(self.webdriver, index=1)

    @property
    def time_period(self):
        return Dropdown(self.webdriver, index=0)

    @property
    def timezone(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def repeat_every_number(self):
        return EditField(self.webdriver, index=2)

    @property
    def repeat_every(self):
        return Dropdown(self.webdriver, index=2)

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-default")

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-primary", index=1)