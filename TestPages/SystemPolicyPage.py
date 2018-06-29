#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.SystemPage import SystemPage
from TestDialogs.PolicyGeneralAddDialog import PolicyGeneralAddDialog
from TestDialogs.PolicyGeneralEditDialog import PolicyGeneralEditDialog
from TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestPages.TestPageObjects.Table.BaseTable import BaseTable
from TestPages.PageEnums import HeadersSystemPolicy
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.PageEnums import State
from TestPages.PageEnums import AlertTo, SwitchAddDialogTabs


class SystemPolicyPage(SystemPage):
    def wait(self):
        system_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.rc-tabs'))
        WebDriverWait(self.webdriver, 20).until(system_page)

    def add_entry(self, service_level, max_mitigation, description=None, switch_tabs=SwitchAddDialogTabs.only_general_tab,
                  service_alerting=State.Disabled, service_subject=None, service_email_body=None, service_alert_to=AlertTo.msp_admins,
                  attack_alerting=State.Disabled, attack_subject=None, attack_email_body=None, attack_alert_to=AlertTo.msp_admins):

        self.create_policy_button.click()
        add_dialog = PolicyGeneralAddDialog(self.webdriver)

        if switch_tabs == SwitchAddDialogTabs.only_general_tab:
            add_dialog.add_entry_and_save(service_level, max_mitigation, description, switch_tabs)
        elif switch_tabs == SwitchAddDialogTabs.general_and_service_level_alerts_tabs:
            add_dialog.add_entry_and_save(service_level, max_mitigation, description, switch_tabs,
                                          service_alerting, service_subject, service_email_body, service_alert_to)
        elif switch_tabs == SwitchAddDialogTabs.general_and_attack_status_alerts_tabs:
            add_dialog.add_entry_and_save(service_level, max_mitigation, description, switch_tabs,
                                          attack_alerting, attack_subject, attack_email_body, attack_alert_to)
        elif switch_tabs == SwitchAddDialogTabs.all_tabs:
            add_dialog.add_entry_and_save(service_level, max_mitigation, description, switch_tabs,
                                          service_alerting, service_subject, service_email_body, service_alert_to,
                                          attack_alerting, attack_subject, attack_email_body, attack_alert_to)
        PrintMessage('Policy created.')

    def edit_entry(self, row, service_level, max_mitigation, description=None, switch_tabs=SwitchAddDialogTabs.only_general_tab,
                   service_alerting=State.Disabled, service_subject=None, service_email_body=None, service_alert_to=AlertTo.msp_admins,
                   attack_alerting=State.Disabled, attack_subject=None, attack_email_body=None, attack_alert_to=AlertTo.msp_admins):

        row.edit_row_item.click()
        edit_dialog = PolicyGeneralEditDialog(self.webdriver)

        if switch_tabs == SwitchAddDialogTabs.only_general_tab:
            edit_dialog.edit_and_confirm(service_level, max_mitigation, description, switch_tabs)
        elif switch_tabs == SwitchAddDialogTabs.general_and_service_level_alerts_tabs:
            edit_dialog.edit_and_confirm(service_level, max_mitigation, description, switch_tabs,
                                         service_alerting, service_subject, service_email_body, service_alert_to)
        elif switch_tabs == SwitchAddDialogTabs.general_and_attack_status_alerts_tabs:
            edit_dialog.edit_and_confirm(service_level, max_mitigation, description, switch_tabs,
                                         attack_alerting, attack_subject, attack_email_body, attack_alert_to)
        elif switch_tabs == SwitchAddDialogTabs.all_tabs:
            edit_dialog.edit_and_confirm(service_level, max_mitigation, description, switch_tabs,
                                         service_alerting, service_subject, service_email_body, service_alert_to,
                                         attack_alerting, attack_subject, attack_email_body, attack_alert_to)

        PrintMessage('Policy edited.')

    def remove_entry(self, service_level):
        row = self.table.get_row_for_field_value(HeadersSystemPolicy.ServiceLevel, service_level)
        self.delete_row(row)

    def delete_row(self, row):
        row.delete_row_item.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        PrintMessage('Policy deleted.')

    @property
    def create_policy_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-primary')

    @property
    def table(self):
        return BaseTable(self.webdriver)

    @property
    def title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.corero-page-title', index=0).get_html()

    @property
    def subtitle(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.corero-page-title', index=1).get_html()

    @property
    def service_policy_and_alerting_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.table-title > div:nth-of-type(1)').get_html()

    @property
    def alerting_not_found_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'h2').get_html()

    @property
    def previous_page(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".glyphicon-chevron-left")

    @property
    def next_page(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".glyphicon-chevron-right")

    @property
    def first_page(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[aria-current='page']", index=0)
