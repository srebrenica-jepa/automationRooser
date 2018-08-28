#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.InitialDashboardPage import InitialDashboardPage


class SmokeTestDashboard(BaseTestClass):
    """
    Original implementation - 27/06/2018
    Updates -
    """
    def setUp(self):
        super(SmokeTestDashboard, self).setUp()

        self.dashboard_page = InitialDashboardPage(self.driver)

    def tearDown(self):
        super(SmokeTestDashboard, self).tearDown()

    def test_C154_CheckDashboardPageDisplayedCorrectly(self):
        # Setup
        title_purchases = 'Purchases summary'
        title_sales = 'Sales summary'

        # Assert
        self.assertEqual(title_purchases, self.dashboard_page.purchases_summary)
        self.assertEqual(title_sales, self.dashboard_page.sales_summary)


