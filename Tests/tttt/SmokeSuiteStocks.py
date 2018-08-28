#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.StocksAllPage import StocksAllPage
from TestPages.CategoriesPage import CategoriesPage
from TestPages.MarketsPage import MarketsPage
from TestPages.TestDialogs.PurchasesAddDialog import PurchasesAddDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import DefaultCut


class SmokeTestStocks(BaseTestClass):
    def setUp(self):
        super(SmokeTestStocks, self).setUp()
        self.all_page = StocksAllPage(self.driver)

        self.market_name = StringMethods.get_unique_name('market_name_')
        self.number_of_doors = StringMethods.get_unique_number()
        self.category_name = StringMethods.get_unique_name('category_name_')

    def tearDown(self):
        super(SmokeTestStocks, self).tearDown()

    def add_category(self, category_name):
        category_page = CategoriesPage(self.driver)
        category_page.add_entry(category_name)

    def remove_category(self, category_name):
        category_page = CategoriesPage(self.driver)
        category_page.remove_entry(category_name)

    def add_market(self, name, number_of_doors):
        markets_page = MarketsPage(self.driver)
        markets_page.add_entry(name, number_of_doors)

    def remove_market(self, name):
        markets_page = MarketsPage(self.driver)
        markets_page.remove_entry(name)

    def test_C144_CheckStocksPageDisplayedCorrectly(self):
        # Setup
        title= 'Stocks'
        subtitle = 'Add new filets'

        self.all_page.wait_for_page()

        # Assert
        self.assertEqual(title, self.all_page.title)
        self.assertEqual(subtitle, self.all_page.subtitle)

    def test_C145_CheckStockAdded(self):
        # fails because a market cannot be added
        # Setup
        cut=DefaultCut.whole
        number_of_boxes = StringMethods.get_unique_digit()
        box_weight = StringMethods.get_unique_digit()
        cost_per_weight = StringMethods.get_unique_digit()

        # Action
        self.add_category(self.category_name)
        self.add_market(self.market_name, self.number_of_doors)
        stocks_page = StocksAllPage(self.driver)
        stocks_page.add_entry(self.market_name, self.category_name, cut, number_of_boxes, box_weight, cost_per_weight)

        # Assert
        stocks_row = stocks_page.table.get_row_for_field_value(TableHeaders.Name, self.market_name)
        self.assertIsNotNone(stocks_row)
        self.assertEqual(self.market_name, stocks_row[TableHeaders.Name])

        stocks_page.remove_entry(self.market_name)

        self.remove_category(self.category_name)
        self.remove_market(self.market_name)

    def test_C146_CheckNoMarketValidation(self):
        # fails because no error message is displayed
        # Setup
        expected_error = 'The market is required'

        # Action
        self.all_page.market.click()
        self.all_page.save_button.click()

        # Assert
        self.all_page.is_text_present(expected_error)

    def test_C147_CheckNoCategoryValidation(self):
        # fails because no error message is displayed
        # Setup
        expected_error = 'The category is required'

        # Action
        self.add_market(self.market_name, self.number_of_doors)
        self.all_page.category.click()
        self.all_page.save_button.click()

        # Assert
        self.all_page.is_text_present(expected_error)

        self.remove_market(self.market_name)

    def test_C148_CheckNoNumberOfBoxesValidation(self):
        # fails because no error message is displayed
        # Setup
        expected_error = 'The number of boxes is required'

        # Action
        self.add_category(self.category_name)
        self.add_market(self.market_name, self.number_of_doors)
        self.all_page.number_of_boxes.click()
        self.all_page.save_button.click()

        # Assert
        self.all_page.is_text_present(expected_error)

        self.remove_category(self.category_name)
        self.remove_market(self.market_name)

    def test_C149_CheckNoBoxWeightValidation(self):
        # fails because no error message is displayed
        # Setup
        expected_error = 'The box weight is required'
        number_of_boxes = StringMethods.get_unique_digit()

        # Action
        self.add_category(self.category_name)
        self.add_market(self.market_name, self.number_of_doors)
        self.all_page.number_of_boxes.send_keys(number_of_boxes)
        self.all_page.box_weight.click()
        self.all_page.save_button.click()

        # Assert
        self.all_page.is_text_present(expected_error)

        self.remove_category(self.category_name)
        self.remove_market(self.market_name)

    def test_C150_CheckNoCostPerKgValidation(self):
        # fails because no error message is displayed
        # Setup
        expected_error = 'The cost per kg is required'
        number_of_boxes = StringMethods.get_unique_digit()
        box_weight = StringMethods.get_unique_digit()

        # Action
        self.add_category(self.category_name)
        self.add_market(self.market_name, self.number_of_doors)
        self.all_page.number_of_boxes.send_keys(number_of_boxes)
        self.all_page.box_weight.send_keys(box_weight)
        self.all_page.cost_per_kg.click()
        self.all_page.save_button.click()

        # Assert
        self.all_page.is_text_present(expected_error)

        self.remove_category(self.category_name)
        self.remove_market(self.market_name)
