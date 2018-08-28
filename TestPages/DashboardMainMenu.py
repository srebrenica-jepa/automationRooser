#!/usr/bin/env python
from TestPages.TestPageObjects.CTAButton import CTAButton
from TestPages.TestPageObjects.InvariableField import InvariableField
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class DashboardMainMenu(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver

    def wait(self):
        menu_present = EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.nav'))
        WebDriverWait(self.webdriver, 20).until(menu_present)

    @property
    def main_menu_dashboard_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(1)")

    @property
    def main_menu_purchases_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(2)")

    @property
    def main_menu_purchases_overview_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(2) > ul > li:nth-child(1)")

    @property
    def main_menu_purchases_all_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(2) > ul > li:nth-child(2)")

    @property
    def main_menu_stocks_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(3)")

    @property
    def main_menu_stocks_all_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(3) > ul > li:nth-child(1)")

    @property
    def main_menu_sales_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(4)")

    @property
    def main_menu_sales_overview_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(4) > ul > li:nth-child(1)")

    @property
    def main_menu_sales_all_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(4) > ul > li:nth-child(2)")

    @property
    def main_menu_dispatch_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(5)")

    @property
    def main_menu_dispatch_overview_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(5) > ul > li:nth-child(1)")

    @property
    def main_menu_dispatch_all_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(5) > ul > li:nth-child(2)")

    @property
    def main_menu_data_lists_button(self):
        return InvariableField(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(6)")

    @property
    def main_menu_users_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(7)")

    @property
    def main_menu_categories_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(8)")

    @property
    def main_menu_products_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(9)")

    @property
    def main_menu_species_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(10)")

    @property
    def main_menu_customers_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(11)")

    @property
    def main_menu_boats_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(12)")

    @property
    def main_menu_offices_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(13)")

    @property
    def main_menu_markets_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(14)")

    @property
    def main_menu_transports_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, "nav > ul > li:nth-child(15)")



















