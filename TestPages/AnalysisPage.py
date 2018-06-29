#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.Dropdown import Dropdown, DropdownSelect


class AnalysisPage(BaseDashboardPage):
    def navigate(self):
        self.wait()
        self.dashboard_object.main_menu_analysis_button.click()
        self.wait_for_page()

    def wait(self):
        header = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.page-default-subheader'))
        WebDriverWait(self.webdriver, 20).until(header)

    def wait_for_page(self):
        analysis_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.container-fluid'))
        WebDriverWait(self.webdriver, 20).until(analysis_page)

    @property
    def print_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.link-button').get_text_without_react()

    @property
    def page_title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.corero-page-title').get_html()

    @property
    def search_by_tenant_name(self):
        return DropdownSelect(self.webdriver, index_of_option=0)

    @property
    def search_by_ip_address(self):
        return DropdownSelect(self.webdriver, index_of_option=1)

    @property
    def search_by_attack_id(self):
        return DropdownSelect(self.webdriver, index_of_option=2)

    @property
    def search_by_asset_name(self):
        return DropdownSelect(self.webdriver, index_of_option=3)

    @property
    def search_by_swa(self):
        return DropdownSelect(self.webdriver, index_of_option=4)

    @property
    def page_subtitle_time_scale(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div:nth-child(4) > div > div.pull-left:nth-child(1) > div > div > label').get_html()

    @property
    def choose_time_scale(self):
        return Dropdown(self.webdriver)

    @property
    def page_subtitle_custom(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div:nth-child(2) > div > div.pull-left:nth-child(1)').get_inner_text()

    @property
    def attacks_title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-child(1) > div:nth-child(1) > .pull-left').get_text_without_react()

