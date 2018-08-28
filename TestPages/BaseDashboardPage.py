from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Common.Utilities.Logging import PrintMessage

from TestPages.DashboardMainMenu import DashboardMainMenu
from TestPages.TestPageObjects.CTAButton import CTAButton


class BaseDashboardPage(object):
    def __init__(self, webdriver):
        self.webdriver = webdriver
        self.dashboard_object = DashboardMainMenu(webdriver)
        self.dashboard_object.wait()
        self.load()

    def perform_logout(self):
        self.wait()
        self.user_profile.click()
        self.logout_button.click()
        PrintMessage('User logged out.')

    def navigate(self):
        return

    def load(self):
        self.navigate()
        self.wait()

    def wait(self):
        user_available = EC.element_to_be_clickable((By.CSS_SELECTOR, '.app-header'))
        WebDriverWait(self.webdriver, 20).until(user_available)

    @property
    def dashboard(self):
        return self.dashboard_object

    @property
    def user_profile(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".user-dropdown")

    @property
    def logout_button(self):
        dropdown_active = EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dropdown"))
        WebDriverWait(self.webdriver, 20).until(dropdown_active)

        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".dropdown-item", index=1)

    @property
    def account_settings_button(self):
        return CTAButton(self.webdriver, By.CSS_SELECTOR, ".dropdown-item")
