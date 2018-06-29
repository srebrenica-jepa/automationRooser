#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from Common.Utilities.Logging import PrintMessage
from TestPages.BaseDashboardPage import BaseDashboardPage
from TestPages.CreateTenantPage import CreateTenantPage
from TestPages.PageEnums import HeadersTenants, SuppressAlerts
from TestPages.SpecificTenantAdministratorsPage import SpecificTenantAdministratorsPage
from TestPages.SpecificTenantDashboardPage import SpecificTenantDashboardPage
from TestPages.SpecificTenantDetailsPage import SpecificTenantDetailsPage
from TestPages.SpecificTenantPage import SpecificTenantPage
from TestPages.SpecificTenantProtectedAssetsPage import SpecificTenantProtectedAssetsPage
from TestPages.TestDialogs.ConfirmDeleteDialog import ConfirmDeleteDialog
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.Dropdown import DropdownMenu, Dropdown
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPages.TestPageObjects.Table.BaseTable import TableType, BaseTable


class SwitchTab(object):
    dashboard_tab = 1
    protected_assets_tab = 2
    asset_groups_tab = 3
    administrators_tab = 4
    details_tab = 5


class TenantsPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_tenants_button.click()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.page-default-subheader'))
        WebDriverWait(self.webdriver, 20).until(header)

    def wait_for_page(self):
        tenants_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-fluid'))
        WebDriverWait(self.webdriver, 20).until(tenants_page)

    def wait_for_main_table(self):
        tenants_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-tenant-list'))
        WebDriverWait(self.webdriver, 20).until(tenants_page)

    def add_entry(self, tenant_name, description, service_level, name, email, status=True, phone=None,
                  address=None, country=None, tab=SwitchTab.dashboard_tab, add_ip=None, add_user=False,
                  admin_email=None, first_name=None, last_name=None, password=None, role=None, admin_phone=None,
                  timezone=None, admin_status=True, suppress_alerts=SuppressAlerts.no_alerts):
        self.create_tenant_button.click()
        add_page = CreateTenantPage(self.webdriver)
        add_page.add_entry_and_save(tenant_name, description, service_level, name, email, status, phone,
                                    address, country)
        PrintMessage('Tenant created.')
        self.select_entry(tenant_name, tab, add_ip, add_user, admin_email, first_name, last_name, password, role,
                          admin_phone, timezone, admin_status, suppress_alerts)

    def edit_entry(self, row, tenant_name, description, service_level, name, email, status=True, phone=None,
                  address=None, country=None):
        row.status_icon.click()
        specific_tenant_page = SpecificTenantPage(self.webdriver)
        specific_tenant_page.details_button.click()
        details_tenant_page = SpecificTenantDetailsPage(self.webdriver)
        details_tenant_page.edit_and_confirm(tenant_name, description, service_level, name, email, status, phone,
                                    address, country)
        PrintMessage('Tenant edited.')

    def select_entry(self, tenant_name, tab=SwitchTab.dashboard_tab, add_ip=None, add_user=False,
                     email=None, first_name=None, last_name=None, password=None, role=None, phone=None,
                     timezone=None, status=True, suppress_alerts=SuppressAlerts.no_alerts):
        self.wait()
        self.webdriver.execute_script("window.scrollTo(0, 0);")
        self.wait()
        row = self.table.get_row_for_field_value(HeadersTenants.Name, tenant_name)
        row.status_icon.click()
        specific_tenant_page = SpecificTenantPage(self.webdriver)
        if tab == SwitchTab.dashboard_tab:
            specific_tenant_page.dashboard_button.click()
            dashboard_tenant_page = SpecificTenantDashboardPage(self.webdriver)
            dashboard_tenant_page.wait()
            dashboard_tenant_page.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        elif tab == SwitchTab.protected_assets_tab:
            specific_tenant_page.protected_assets_button.click()
            protected_assets_tenant_page = SpecificTenantProtectedAssetsPage(self.webdriver)
            protected_assets_tenant_page.wait()
            protected_assets_tenant_page.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if add_ip:
                protected_assets_tenant_page.add_entry(ip_address=add_ip)

        elif tab == SwitchTab.asset_groups_tab:
            specific_tenant_page.asset_groups_button.click()
            #asset_groups_tenant_page =

        elif tab == SwitchTab.administrators_tab:
            specific_tenant_page.administrators_button.click()
            administrators_tenant_page = SpecificTenantAdministratorsPage(self.webdriver)
            administrators_tenant_page.wait()
            administrators_tenant_page.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            if add_user:
                administrators_tenant_page.add_entry(email, first_name, last_name, password, role, phone, timezone,
                                                     status, suppress_alerts)

        elif tab == SwitchTab.details_tab:
            specific_tenant_page.details_button.click()
            details_tenant_page = SpecificTenantDetailsPage(self.webdriver)
            details_tenant_page.wait()
            details_tenant_page.webdriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def remove_entry(self, tenant_name):
        self.webdriver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        row = self.table.get_row_for_field_value(HeadersTenants.Name, tenant_name)
        row.status_icon.click()
        specific_tenant_page = SpecificTenantPage(self.webdriver)
        specific_tenant_page.delete_tenant_button.click()
        delete_dialog = ConfirmDeleteDialog(self.webdriver)
        delete_dialog.confirm_delete.click()
        PrintMessage('Tenant deleted.')

    @property
    def create_tenant_button(self):
        return CTAButton(self.webdriver, by_type=By.CSS_SELECTOR, value='.btn.btn-info')

    @property
    def import_tenants(self):
        return DropdownMenu(self.webdriver, index=1, index_of_option=3)

    @property
    def import_assets(self):
        return DropdownMenu(self.webdriver, index=1, index_of_option=4)

    @property
    def admin_status(self):
        return Dropdown(self.webdriver)

    @property
    def attack_status(self):
        return Dropdown(self.webdriver, index=1)

    @property
    def service_level(self):
        return Dropdown(self.webdriver, index=2)

    @property
    def table(self):
        return BaseTable(self.webdriver, table_type=TableType.status_action_type)

    @property
    def page_title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.corero-page-title').get_html()

    @property
    def subtitle_admin_status(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > form > div:nth-child(1) > label').get_html()

    @property
    def subtitle_attack_status(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > form > div:nth-child(2) > label').get_html()

    @property
    def subtitle_service_level(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > form > div:nth-child(3) > div > label').get_html()






