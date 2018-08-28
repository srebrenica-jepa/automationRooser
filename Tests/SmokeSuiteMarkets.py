#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.MarketsPage import MarketsPage
from TestPages.TestDialogs.MarketsAddDialog import MarketsAddDialog
from TestPages.TestDialogs.MarketsCheckDialog import MarketsCheckDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import HeadersMarkets


class SmokeTestMarkets(BaseTestClass):
    def setUp(self):
        super(SmokeTestMarkets, self).setUp()
        self.markets_page = MarketsPage(self.driver)

    def tearDown(self):
        super(SmokeTestMarkets, self).tearDown()

    def test_C12_CheckMarketsPageDisplayedCorrectly(self):
        # Setup
        title = 'Markets'
        subtitle = 'Manage markets information.'

        # Assert
        self.assertEqual(title, self.markets_page.title)
        self.assertEqual(subtitle, self.markets_page.subtitle)

    def test_C13_CheckMarketAdded(self):
        # fails due to raised error
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = StringMethods.get_unique_digit()
        market_cost = StringMethods.get_unique_number()

        self.addCleanup(self.markets_page.remove_entry, market_name)

        # Action
        self.markets_page.add_entry(market_name, number_of_doors, delivery_time, market_cost)

        # Assert
        market_row = self.markets_page.table.get_row_for_field_value(HeadersMarkets.Name, market_name)
        self.assertIsNotNone(market_row)
        self.assertEqual(market_name, market_row[HeadersMarkets.Name])
        self.assertEqual(number_of_doors, market_row[HeadersMarkets.NumberOfDoors])
        self.assertEqual(delivery_time, market_row[HeadersMarkets.DeliveryTime])

    def test_C14_CheckMarketEdited(self):
        # fails and unable to test because of C13
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = StringMethods.get_unique_digit()
        market_cost = StringMethods.get_unique_number()

        # Setup - edit
        market_name_edited = StringMethods.get_unique_name('market_name_')
        number_of_doors_edited = StringMethods.get_unique_number()
        delivery_time_edited = StringMethods.get_unique_digit()
        market_cost_edited = StringMethods.get_unique_number()

        self.addCleanup(self.markets_page.remove_entry, market_name_edited)

        # Action
        self.markets_page.add_entry(market_name, number_of_doors, delivery_time, market_cost)
        markets_row = self.markets_page.table.get_row_for_field_value(HeadersMarkets.Name, market_name)
        self.markets_page.edit_entry(markets_row, market_name_edited, number_of_doors_edited, delivery_time_edited, market_cost_edited)

        # Assert
        self.markets_page.wait_for_page()
        markets_row = self.markets_page.table.get_row_for_field_value(HeadersMarkets.Name, market_name_edited)
        self.assertIsNotNone(markets_row)
        self.assertEqual(market_name_edited, markets_row[HeadersMarkets.Name])

    def test_C15_CheckMarketRemoved(self):
        # fails and unable to test because of C13
        # Setup
        no_markets_message = 'There is no data to display'
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()

        # Action
        self.markets_page.add_entry(market_name, number_of_doors)
        markets_row = self.markets_page.table.get_row_for_field_value(HeadersMarkets.Name, market_name)
        self.markets_page.delete_row(markets_row)

        # Assert
        self.assertEqual(no_markets_message, self.markets_page.empty_text)

    def test_C16_CheckNewMarketRightDetails(self):
        # fails and unable to test because of C13
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = StringMethods.get_unique_digit()
        market_cost = StringMethods.get_unique_number()

        # Action
        self.markets_page.add_entry(market_name, number_of_doors, delivery_time, market_cost)
        market_row = self.markets_page.table.get_row_for_field_value(HeadersMarkets.Name, market_name)
        market_row.details_row_item.click()
        check_dialog = MarketsCheckDialog(self.driver)

        # Assert
        self.assertEqual(market_name, check_dialog.market_name)

        check_dialog.remove_entry(market_name)

    def test_C17_CheckMarketDetailsThenEdit(self):
        # fails and unable to test because of C13
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = StringMethods.get_unique_digit()
        market_cost = StringMethods.get_unique_number()

        # Setup - edit
        market_name_edited = StringMethods.get_unique_name('market_name_')
        number_of_doors_edited = StringMethods.get_unique_number()
        delivery_time_edited = StringMethods.get_unique_digit()
        market_cost_edited = StringMethods.get_unique_number()

        self.addCleanup(self.markets_page.remove_entry, market_name_edited)

        # Action
        self.markets_page.add_entry(market_name, number_of_doors, delivery_time, market_cost)

        market_row = self.markets_page.table.get_row_for_field_value(HeadersMarkets.Name, market_name)
        market_row.details_row_item.click()
        check_dialog = MarketsCheckDialog(self.driver)
        check_dialog.edit_entry(market_name_edited, number_of_doors_edited, delivery_time_edited, market_cost_edited)

        # Assert
        market_row = self.markets_page.table.get_row_for_field_value(HeadersMarkets.Name, market_name_edited)
        self.assertIsNotNone(market_row)
        self.assertEqual(market_name_edited, market_row[HeadersMarkets.Name])

    def test_C18_CheckMarketDetailsThenDelete(self):
        # fails and unable to test because of C13
        # Setup
        no_market_message = 'There is no data to display'
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = StringMethods.get_unique_digit()
        market_cost = StringMethods.get_unique_number()
        market_name = StringMethods.get_unique_name('market_name_')

        # Action
        self.markets_page.add_entry(market_name, number_of_doors, delivery_time, market_cost)

        market_row = self.markets_page.table.get_row_for_field_value(HeadersMarkets.Name, market_name)
        market_row.details_row_item.click()
        check_dialog = MarketsCheckDialog(self.driver)
        check_dialog.remove_entry(market_name)

        # Assert
        self.assertEqual(no_market_message, self.markets_page.empty_text)

    def test_C19_CheckNoMarketNameValidation(self):
        # fails due to no cancel button
        # Setup
        expected_error = 'Market name is required'

        # Action
        self.markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C20_CheckIncorrectMarketNameValidation(self):
        # fails due to no cancel button
        # Setup
        market_name = '@'
        expected_error = 'Please enter a name of at least 5 characters'

        # Action
        self.markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.send_keys(market_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C119_CheckNoNumberOfDoorsValidation(self):
        # fails due to no cancel button
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        expected_error = 'Number of doors is required'

        # Action
        self.markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.send_keys(market_name)
        add_dialog.number_of_doors.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C20_CheckIncorrectNumberOfDoorsValidation(self):
        # fails due to no cancel button
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = 'e'
        expected_error = 'Please enter a valid number'

        # Action
        self.markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.send_keys(market_name)
        add_dialog.number_of_doors.send_keys(number_of_doors)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C23_CheckIncorrectDeliveryTimeValidation(self):
        # fails due to no cancel button
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = 'e'
        expected_error = 'Please enter a valid number'

        # Action
        self.markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.send_keys(market_name)
        add_dialog.number_of_doors.send_keys(number_of_doors)
        add_dialog.delivery_time.send_keys(delivery_time)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C22_CheckIncorrectDeliveryTimeLess0Validation(self):
        # fails due to no cancel button
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = '-1'
        expected_error = 'Please enter a value greater than or equal to 0.'

        # Action
        self.markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.send_keys(market_name)
        add_dialog.number_of_doors.send_keys(number_of_doors)
        add_dialog.delivery_time.send_keys(delivery_time)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C118_CheckIncorrectMarketCostValidation(self):
        # fails due to no cancel button
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = StringMethods.get_unique_digit()
        market_cost = 'e'
        expected_error = 'Please enter a valid number'

        # Action
        self.markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.send_keys(market_name)
        add_dialog.number_of_doors.send_keys(number_of_doors)
        add_dialog.delivery_time.send_keys(delivery_time)
        add_dialog.market_cost.send_keys(market_cost)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C106_CheckIncorrectMarketCostLess0Validation(self):
        # fails due to no cancel button
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = StringMethods.get_unique_digit()
        market_cost = '-1'
        expected_error = 'Please enter a value greater than or equal to 0.'

        # Action
        self.markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.send_keys(market_name)
        add_dialog.number_of_doors.send_keys(number_of_doors)
        add_dialog.delivery_time.send_keys(delivery_time)
        add_dialog.market_cost.send_keys(market_cost)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C107_CheckNoDuplicateEntriesAllowed(self):
        # fails and unable to test because of C13
        # Setup
        market_name = StringMethods.get_unique_name('market_name_')
        number_of_doors = StringMethods.get_unique_number()
        delivery_time = StringMethods.get_unique_digit()
        market_cost = StringMethods.get_unique_number()

        expected_error = 'Duplicate entries are not allowed.'

        # Action
        self.markets_page.add_entry(market_name, number_of_doors, delivery_time, market_cost)
        markets_page = MarketsPage(self.driver)
        markets_page.add_button.click()
        add_dialog = MarketsAddDialog(self.driver)
        add_dialog.name.send_keys(market_name)
        add_dialog.number_of_doors.send_keys(number_of_doors)
        add_dialog.delivery_time.send_keys(delivery_time)
        add_dialog.market_cost.send_keys(market_cost)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()
        markets_page.remove_entry(market_name)