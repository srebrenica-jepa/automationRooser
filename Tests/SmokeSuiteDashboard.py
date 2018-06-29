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
        super(SmokeTestAnalysis, self).tearDown()

    def test_C72830_CheckAnalysisPageDisplayedCorrectly(self):
        # Setup
        title = 'Attack Analysis'
        subtitle_time_scale = 'Choose Time Scale:'
        subtitle_custom = 'Custom:'
        print_text = 'Print'
        attacks_text = 'Attacks '

        # Assert
        self.assertEqual(title, self.analysis_page.page_title)
        self.assertEqual(subtitle_time_scale, self.analysis_page.page_subtitle_time_scale)
        self.assertEqual(subtitle_custom, self.analysis_page.page_subtitle_custom)
        self.assertEqual(print_text, self.analysis_page.print_text)
        self.assertEqual(attacks_text, self.analysis_page.attacks_title)

    def test_C80484_CheckDefaultDropdownSearchingByTenantName(self):
        # Setup
        tenant_name = 'Tenant Name'

        # Assert
        self.assertEqual(tenant_name, self.analysis_page.search_by_attack_id)

    def test_C80485_CheckAllDropdownValuesSearchingCorrectlyDisplayed(self):
        # Setup
        tenant_name = 'Tenant Name'
        ip_address = 'IP Address'
        attack_id = 'Attack ID'
        asset_name = 'Asset Name'
        splunk_server = 'SWA'

        # Assert
        self.assertEqual(tenant_name, self.analysis_page.search_by_tenant_name)
        self.assertEqual(ip_address, self.analysis_page.search_by_ip_address)
        self.assertEqual(attack_id, self.analysis_page.search_by_attack_id)
        self.assertEqual(asset_name, self.analysis_page.search_by_asset_name)
        self.assertEqual(splunk_server, self.analysis_page.search_by_swa)

    def test_C80486_CheckDefaultValueTimeScaleIsLastHour(self):
        # Setup
        last_hour = 'Last Hour'

        # Assert
        self.assertEqual(last_hour, self.analysis_page.choose_time_scale.current_value)

    def test_C80487_CheckAllTimeScalesCorrectlyDisplayed(self):
        # Setup
        last_hour = 'Last Hour'
        day = '24 Hours'
        week = '7 Days'
        month = '30 Days'

        # Action and Assert
        self.assertEqual(last_hour, self.analysis_page.choose_time_scale.current_value)
        self.analysis_page.choose_time_scale.select_input(day)
        self.assertEqual(day, self.analysis_page.choose_time_scale.current_value)
        self.analysis_page.choose_time_scale.select_input(week)
        self.assertEqual(week, self.analysis_page.choose_time_scale.current_value)
        self.analysis_page.choose_time_scale.select_input(month)
        self.assertEqual(month, self.analysis_page.choose_time_scale.current_value)

    def test_C82426_CheckSearchingByIPAddress(self):
        # Setup
        ip_address = 'IP Address'


        # Assert
        self.assertEqual(tenant_name, self.analysis_page.search_by_tenant_name)

