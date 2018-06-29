#!/usr/bin/env python
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from TestPages.BaseDashboardPage import BaseDashboardPage
from TestPages.TestPageObjects.InvariableField import InvariableField
from TestPageObjects.Dropdown import Dropdown


class OverviewPage(BaseDashboardPage):
    def wait(self):
        overview_page = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#page-overview'))
        WebDriverWait(self.webdriver, 20).until(overview_page)

    @property
    def print_text(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.link-button').get_text_without_react()

    @property
    def page_title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, '.corero-page-title').get_html()

    @property
    def page_subtitle(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div:nth-child(2) > div > div:nth-child(1) > div > div > label').get_html()

    @property
    def choose_time_scale(self):
        return Dropdown(self.webdriver)

    @property
    def inbound_traffic_title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-child(1) > div:nth-child(1) > .pull-left').get_html()

    @property
    def top_attacked_tenants_title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-child(1) > div:nth-child(1) > .pull-left', index=1).get_inner_text()

    @property
    def top_attacked_ip_addresses_title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div:nth-child(1) > div:nth-child(2) > div:nth-child(2) > div:nth-child(2) > div:nth-child(1) > .pull-left').get_inner_text()

    @property
    def attacks_title(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, 'div > div:nth-child(1) > div:nth-child(1) > .pull-left', index=2).get_text_without_react()

