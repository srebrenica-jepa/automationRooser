#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Common.Utilities.Logging import PrintMessage

from TestPages.SystemPage import SystemPage
from TestDialogs.LDAPServerAddDialog import LDAPServerAddDialog
from TestDialogs.LDAPServerEditDialog import LDAPServerEditDialog
from TestDialogs.LDAPGroupRoleMappingAddDialog import LDAPGroupRoleMappingAddDialog
from TestDialogs.LDAPGroupRoleMappingEditDialog import LDAPGroupRoleMappingEditDialog
from TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestPages.PageActions.NotificationVerifier import NotificationVerifier
from TestPages.TestPageObjects.Table.BaseTable import BaseTable
from TestPages.PageEnums import HeadersSystemLDAPServers, HeadersSystemLDAPGroupRoleMapping
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPageObjects.Dropdown import Dropdown
from TestPageObjects.EditField import EditField


class SystemLDAPPage(SystemPage, NotificationVerifier):
    def wait(self):
        system_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-sync'))
        WebDriverWait(self.webdriver, 50).until(system_page)

    def add_entry_server(self, name, connection_type, host, port, connection_timeout, request_timeout):
        self.wait()
        self.add_server_button.click()
        add_dialog = LDAPServerAddDialog(self.webdriver)
        add_dialog.add_entry(name, connection_type, host, port, connection_timeout, request_timeout)
        PrintMessage('LDAP created.')

    def edit_entry_server(self, row, connection_type, host, port, connection_timeout, request_timeout):
        self.wait()
        row.edit_row_item.click()
        edit_dialog = LDAPServerEditDialog(self.webdriver)
        edit_dialog.edit_entry(connection_type, host, port, connection_timeout, request_timeout)
        PrintMessage('LDAP edited.')

    def remove_entry_server(self, name):
        self.wait()
        row = self.servers_table.get_row_for_field_value(HeadersSystemLDAPServers.Name, name)
        self.delete_row_server(row)

    def delete_row_server(self, row):
        row.delete_row_item.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        PrintMessage('LDAP deleted.')

    def add_entry_group_role_mapping(self, ldap_group, role):
        self.wait()
        self.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        self.add_mapping_button.click()
        add_dialog = LDAPGroupRoleMappingAddDialog(self.webdriver)
        add_dialog.add_entry(ldap_group, role)
        PrintMessage('Group Role Mapping created.')

    def edit_entry_group_role_mapping(self, row, role):
        self.wait()
        self.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        row.edit_row_item.click()
        edit_dialog = LDAPGroupRoleMappingEditDialog(self.webdriver)
        edit_dialog.edit_entry(role)
        PrintMessage('Group Role Mapping edited.')

    def remove_entry_group_role_mapping(self, group):
        self.wait()
        row = self.group_role_mapping_table.get_row_for_field_value(HeadersSystemLDAPGroupRoleMapping.LDAPGroup, group)
        self.delete_row_group(row)

    def delete_row_group(self, row):
        row.delete_row_item.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        PrintMessage('Group Role Mapping deleted.')

    @property
    def set_options_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-primary', index=0)

    @property
    def add_server_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-primary', index=1)

    @property
    def add_mapping_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-primary', index=2)

    @property
    def sync_now_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-primary', index=3)

    @property
    def set_schedule_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, '.btn-primary', index=4)

    @property
    def servers_table(self):
        return BaseTable(self.webdriver)

    @property
    def group_role_mapping_table(self):
        return BaseTable(self.webdriver, index=1)

    @property
    def ldap_options_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'h3', index=0).get_html()

    @property
    def ldap_global_attributes_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-of-type(1) > h5').get_html()

    @property
    def admin_state_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(1) > div:nth-of-type(1)').get_html()

    @property
    def bind_dn_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > form > div > div:nth-of-type(1)').get_html()

    @property
    def bind_dn(self):
        return EditField(self.webdriver)

    @property
    def bind_dn_password_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(1)').get_html()

    @property
    def bind_dn_password(self):
        return EditField(self.webdriver, index=1)

    @property
    def ldap_user_attributes_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-of-type(2) > h5').get_html()

    @property
    def user_name_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(1) > div:nth-of-type(1)').get_html()

    @property
    def real_name_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2) > div:nth-of-type(1)').get_html()

    @property
    def email_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(3) > div:nth-of-type(1)').get_html()

    @property
    def user_base_dn_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(4) > div:nth-of-type(1)').get_html()

    @property
    def user_search_filter_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(5) > div:nth-of-type(1)').get_html()

    @property
    def ldap_group_attributes_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-of-type(3) > h5').get_html()

    @property
    def group_name_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(1) > div:nth-of-type(1)').get_html()

    @property
    def group_mapping_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(2) > div:nth-of-type(1)').get_html()

    @property
    def group_member_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(3) > div:nth-of-type(1)').get_html()

    @property
    def group_base_dn_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(4) > div:nth-of-type(1)').get_html()

    @property
    def group_search_filter_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.container-sync > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(3) > div > div:nth-of-type(5) > div:nth-of-type(1)').get_html()

    @property
    def ldap_servers_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'h3', index=1).get_html()

    @property
    def group_role_mapping_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'h3', index=2).get_html()

    @property
    def ldap_synchronization_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'h3', index=3).get_html()

    @property
    def repeat_every_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.ldap-sync > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1) > div').get_html()

    @property
    def repeat_every(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def start_at_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.ldap-sync > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1)').get_html()

    @property
    def last_sync_attempt_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-of-type(3) > h3').get_html()

    @property
    def last_sync_time_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-of-type(3) > ul > li:nth-of-type(1)').get_text_without_react()

    @property
    def total_ldap_users_found_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-of-type(3) > ul > li:nth-of-type(2)').get_text_without_react()

    @property
    def sync_details_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-of-type(3) > ul > li:nth-of-type(3)').get_text_without_react()

    @property
    def sync_errors_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-of-type(3) > ul > li:nth-of-type(4)').get_text_without_react()

    @property
    def previous_page(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".glyphicon-chevron-left")

    @property
    def next_page(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".glyphicon-chevron-right")

    @property
    def first_page(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "[aria-current='page']", index=0)

    @property
    def no_servers_found_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div.container-default:nth-of-type(2) > div > div > div > div > div > div > div > div > div > div > div > div > h2').get_html()

    @property
    def no_group_role_mapping_found_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div.container-default:nth-of-type(3) > div > div > div > div > div > div > div > div > div > div > div > div > h2').get_html()
