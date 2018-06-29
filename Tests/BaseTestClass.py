#!/usr/bin/env python
import unittest

from selenium import webdriver

from Common.Utilities import DiskTools
from Common.Utilities.Logging import PrintMessage
from ConfigFiles import Constants as Const
from TestHelpers import StringMethods
from TestPages.BaseDashboardPage import BaseDashboardPage
from TestPages.LoginPage import LoginPageForm


SCREENSHOTS_FOLDER = './screenshots/'
SCREENSHOT_NAME = "{0}{1}{2}.png"


class BaseTestClass(unittest.TestCase):
    driver = None

    @classmethod
    def setUpClass(cls):
        cls.longMessage = True

    def setUp(self):
        PrintMessage(Const.TEST_HEAD.format(self._testMethodName))

        # Firefox Setup
        # caps = webdriver.DesiredCapabilities().FIREFOX
        # caps["marionette"] = False
        # self.driver = webdriver.Firefox(capabilities=caps)
        # self.driver.maximize_window()

        # Chrome Setup
        self.driver = webdriver.Chrome(executable_path='/afs/inf.ed.ac.uk/user/s12/s1211898/miniconda3/envs/automationRooser/selenium/webdriver/chromedriver')
        self.driver.maximize_window()

        login_page = LoginPageForm(self.driver)
        login_page.perform_login('oana@rooser.co.uk', 'helloworld123')

        self.addCleanup(self.driver.quit)
        self.addCleanup(self.driver.close)
        self.addCleanup(self.perform_log_out)

    def tearDown(self):
        PrintMessage(Const.TEST_TAIL)

    def run(self, result=None):
        super(BaseTestClass, self).run(TestResultEx(result, self))

    def perform_log_out(self):
        # self.driver.refresh()
        dashboard = BaseDashboardPage(self.driver)
        dashboard.perform_logout()


class TestResultEx(object):
    def __init__(self, result, test_case):
        DiskTools.create_folder(SCREENSHOTS_FOLDER)
        self.result = result
        self.test_case = test_case

    def __getattr__(self, name):
        return object.__getattribute__(self.result, name)

    def get_screenshot_name(self, failure_type):
        return SCREENSHOT_NAME.format(SCREENSHOTS_FOLDER,
                                      self.test_case._testMethodName,
                                      StringMethods.get_unique_string(failure_type))

    def addError(self, test, err):
        self.result.addError(test, err)
        file_name = self.get_screenshot_name('_error')
        if self.test_case.driver:
            self.test_case.driver.save_screenshot(file_name)

    def addFailure(self, test, err):
        self.result.addFailure(test, err)
        file_name = self.get_screenshot_name('_failure')
        if self.test_case.driver:
            self.test_case.driver.save_screenshot(file_name)
