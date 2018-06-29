#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.TestDialogs.PolicyDialog import PolicyDialog
from TestPages.TestDialogs.PolicyServiceLevelAlertsAddDialog import PolicyServiceLevelAlertsAddDialog
from TestPages.TestDialogs.PolicyAttackStatusAlertsAddDialog import PolicyAttackStatusAlertsAddDialog#
from TestPages.PageEnums import State
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.EditField import EditField
from TestPages.PageActions.NotificationVerifier import NotificationVerifier
from TestPages.PageEnums import AlertTo, SwitchAddDialogTabs


class PolicyGeneralAddDialog(PolicyDialog, NotificationVerifier):
    def __init__(self, webdriver):
        super(PolicyGeneralAddDialog, self).__init__(webdriver)

        self.webdriver = webdriver
        self.wait()

    def wait(self):
        add_dialog = EC.presence_of_all_elements_located((By.CLASS_NAME, 'modal-body'))
        WebDriverWait(self.webdriver, 10).until(add_dialog)

    def add_service_level_alerts_entry(self, alerting, subject=None, email_body=None, alert_to=AlertTo.msp_admins):
        self.service_level_alerts_button.click()
        add_dialog = PolicyServiceLevelAlertsAddDialog(self.webdriver)
        add_dialog.add_entry(alerting, subject, email_body, alert_to)

    def add_attack_status_alerts_entry(self, alerting, subject=None, email_body=None, alert_to=AlertTo.msp_admins):
        self.attack_status_alerts_button.click()
        add_dialog = PolicyAttackStatusAlertsAddDialog(self.webdriver)
        add_dialog.add_entry(alerting, subject, email_body, alert_to)

    def add_entry_and_save(self, service_level, max_mitigation, description=None, switch_tabs=SwitchAddDialogTabs.only_general_tab,
                           service_alerting=State.Disabled, service_subject=None, service_email_body=None, service_alert_to=AlertTo.msp_admins,
                           attack_alerting=State.Disabled, attack_subject=None, attack_email_body=None, attack_alert_to=AlertTo.msp_admins):
        self.wait()

        self.service_level.send_keys(service_level)
        self.max_mitigation.send_keys(max_mitigation)
        if description:
            self.description.send_keys(description)

        if switch_tabs == SwitchAddDialogTabs.general_and_service_level_alerts_tabs:
            self.add_service_level_alerts_entry(service_alerting, service_subject, service_email_body, service_alert_to)
        elif switch_tabs == SwitchAddDialogTabs.general_and_attack_status_alerts_tabs:
            self.add_attack_status_alerts_entry(attack_alerting, attack_subject, attack_email_body, attack_alert_to)
        elif switch_tabs == SwitchAddDialogTabs.all_tabs:
            self.add_service_level_alerts_entry(service_alerting, service_subject, service_email_body, service_alert_to)
            self.add_attack_status_alerts_entry(attack_alerting, attack_subject, attack_email_body, attack_alert_to)

        self.save_button.click()

    @property
    def service_level(self):
        return EditField(self.webdriver, index=0)

    @property
    def max_mitigation(self):
        return EditField(self.webdriver, index=1)

    @property
    def description(self):
        return EditField(self.webdriver, index=2)

    @property
    def cancel_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-default")

    @property
    def save_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".btn-primary", index=1)
