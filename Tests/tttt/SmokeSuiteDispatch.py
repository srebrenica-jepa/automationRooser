#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.DispatchAllPage import DispatchAllPage
from TestPages.DispatchOverviewPage import DispatchOverviewPage
from TestHelpers import StringMethods


class SmokeTestDispatch(BaseTestClass):
    def setUp(self):
        super(SmokeTestDispatch, self).setUp()
        self.overview_page = DispatchOverviewPage(self.driver)
        self.all_page = DispatchAllPage(self.driver)

    def tearDown(self):
        super(SmokeTestDispatch, self).tearDown()

    def test_C124_CheckDispatchOverviewPageDisplayedCorrectly(self):
        # Setup
        title_summary = 'Dispatch Summary'
        title_transport = 'Transport Manifests'

        self.overview_page.wait_for_page()

        # Assert
        self.assertEqual(title_summary, self.overview_page.title_summary)
        self.assertEqual(title_transport, self.overview_page.title_transport)

    def test_C125_CheckDispatchAllPageDisplayedCorrectly(self):
        # Setup
        title = 'Dispatches'
        button = ' Refresh'

        self.all_page.wait()

        # Assert
        self.assertEqual(title, self.all_page.title)
        self.assertEqual(button, self.all_page.refresh_button_text)