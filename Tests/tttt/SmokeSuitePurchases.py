#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.PurchasesAllPage import PurchasesAllPage
from TestPages.PurchasesOverviewPage import PurchasesOverviewPage
from TestPages.SpeciesPage import SpeciesPage
from TestPages.BoatsPage import BoatsPage
from TestPages.MarketsPage import MarketsPage
from TestPages.OfficesPage import OfficesPage
from TestPages.TestDialogs.PurchasesAddDialog import PurchasesAddDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import HeadersPuchases


class SmokeTestPurchases(BaseTestClass):
    def setUp(self):
        super(SmokeTestPurchases, self).setUp()
        self.overview_page = PurchasesOverviewPage(self.driver)
        self.all_page = PurchasesAllPage(self.driver)

        self.species_name = StringMethods.get_unique_name('species_name_')
        self.market_name = StringMethods.get_unique_name('market_name_')
        self.number_of_doors = StringMethods.get_unique_number()
        self.office_name = StringMethods.get_unique_name('office_name_')
        self.boat_name = StringMethods.get_unique_name('boat_name_')

    def tearDown(self):
        super(SmokeTestPurchases, self).tearDown()

    def add_office(self, office_name):
        office_page = OfficesPage(self.driver)
        office_page.add_entry(office_name)

    def remove_office(self, office_name):
        office_page = OfficesPage(self.driver)
        office_page.remove_entry(office_name)

    def add_species(self, name):
        species_page = SpeciesPage(self.driver)
        species_page.add_entry(name)

    def remove_species(self, name):
        species_page = SpeciesPage(self.driver)
        species_page.remove_entry(name)

    def add_market(self, name, number_of_doors):
        markets_page = MarketsPage(self.driver)
        markets_page.add_entry(name, number_of_doors)

    def remove_market(self, name):
        markets_page = MarketsPage(self.driver)
        markets_page.remove_entry(name)

    def add_boat(self, name, office):
        boat_page = BoatsPage(self.driver)
        boat_page.add_entry(name, office)

    def remove_boat(self, name):
        boat_page = BoatsPage(self.driver)
        boat_page.remove_entry(name)

    def test_C127_CheckPurchasesOverviewPageDisplayedCorrectly(self):
        # Setup
        title_by_office = 'Day Purchases by Office'
        title_by_species = 'Week Purchases by Species'

        self.overview_page.wait_for_page()

        # Assert
        self.assertEqual(title_by_office, self.overview_page.title_by_office)
        self.assertEqual(title_by_species, self.overview_page.title_by_species)

    def test_C128_CheckPurchasesAllPageDisplayedCorrectly(self):
        # Setup
        title = 'Purchases'

        self.all_page.wait()

        # Assert
        self.assertEqual(title, self.all_page.title)

    def test_C131_CheckPurchaseAdded(self):
        # fails because we cannot add a market
        # Setup
        date = StringMethods.get_unique_date()
        no_boxes = StringMethods.get_unique_digit()
        kg = StringMethods.get_unique_digit()
        cost = StringMethods.get_unique_digit()

        # Action
        self.add_office(self.office_name)
        self.add_boat(self.boat_name, self.office_name)

        self.add_species(self.species_name)
        self.add_market(self.market_name,self.number_of_doors)

        purchases_page = PurchasesAllPage(self.driver)
        purchases_page.add_entry(date, no_boxes, kg, cost, self.species_name, self.market_name, market_door, self.boat_name)

        # Assert
        purchases_row = purchases_page.table.get_row_for_field_value(HeadersPuchases.PassedAt, date)
        self.assertIsNotNone(purchases_row)
        self.assertEqual(date, purchases_row[HeadersPuchases.PassedAt])

        purchases_page.remove_entry(date)

        self.remove_market(self.market_name)
        self.remove_species(self.species_name)
        self.remove_boat(self.boat_name)
        self.remove_office(self.office_name)

    def test_C132_CheckPurchaseEdited(self):
        # fails because we cannot add a market
        # Setup
        date = StringMethods.get_unique_date()
        no_boxes = StringMethods.get_unique_digit()
        kg = StringMethods.get_unique_digit()
        cost = StringMethods.get_unique_digit()

        # Setup -edited
        date_edited = StringMethods.get_unique_date()
        no_boxes_edited = StringMethods.get_unique_digit()
        kg_edited = StringMethods.get_unique_digit()
        cost_edited = StringMethods.get_unique_digit()

        # Action
        self.add_office(self.office_name)
        self.add_boat(self.boat_name, self.office_name)

        self.add_species(self.species_name)
        self.add_market(self.market_name,self.number_of_doors)

        purchases_page = PurchasesAllPage(self.driver)
        purchases_page.add_entry(date, no_boxes, kg, cost, self.species_name, self.market_name, market_door, self.boat_name)
        purchases_row = purchases_page.table.get_row_for_field_value(HeadersPuchases.PassedAt, date)
        purchases_page.edit_entry(date_edited, no_boxes_edited, kg_edited, cost_edited, self.species_name, self.market_name, market_door, self.boat_name)

        # Assert
        purchases_row = purchases_page.table.get_row_for_field_value(HeadersPuchases.PassedAt, date_edited)

        self.assertIsNotNone(purchases_row)
        self.assertEqual(date_edited, purchases_row[HeadersPuchases.PassedAt])

        purchases_page.remove_entry(date_edited)

        self.remove_market(self.market_name)
        self.remove_species(self.species_name)
        self.remove_boat(self.boat_name)
        self.remove_office(self.office_name)

    def test_C133_CheckNoPurchaseDateValidation(self):
        # fails because no error message
        # Setup
        expected_error = 'Purchase date is required.'
        no_boxes = StringMethods.get_unique_digit()

        # Action
        self.all_page.add_button.click()
        add_dialog = PurchasesAddDialog(self.driver)
        add_dialog.date.click()
        add_dialog.date.clear()
        add_dialog.no_boxes.send_keys(no_boxes)
        add_dialog.save_button.click()

        # Assert
        self.assertEqual(expected_error, add_dialog.error)

        add_dialog.cancel_button.click()

    def test_C134_CheckIncorrectPurchaseDateValidation(self):
        # fails because no error message
        # Setup
        expected_error = 'Please enter a purchase date in the correct format.'
        no_boxes = StringMethods.get_unique_digit()
        date = '@'

        # Action
        self.all_page.add_button.click()
        add_dialog = PurchasesAddDialog(self.driver)
        add_dialog.date.click()
        add_dialog.date.clear()
        add_dialog.date.send_keys(date)
        add_dialog.no_boxes.send_keys(no_boxes)
        add_dialog.save_button.click()

        # Assert
        self.assertEqual(expected_error, add_dialog.error)

        add_dialog.cancel_button.click()

    def test_C139_CheckNoSpeciesValidation(self):
        # Setup
        expected_error = 'The species_id field is required.'
        no_boxes = StringMethods.get_unique_digit()
        kg = StringMethods.get_unique_digit()
        cost = StringMethods.get_unique_digit()

        # Action
        self.all_page.add_button.click()
        add_dialog = PurchasesAddDialog(self.driver)
        add_dialog.no_boxes.send_keys(no_boxes)
        add_dialog.kg.send_keys(kg)
        add_dialog.cost.send_keys(cost)
        add_dialog.save_button.click()

        # Assert
        self.assertEqual(expected_error, add_dialog.error)

        add_dialog.cancel_button.click()

    def test_C143_CheckNoBoatValidation(self):
        # Setup
        expected_error = 'The boat_id field is required.'
        no_boxes = StringMethods.get_unique_digit()
        kg = StringMethods.get_unique_digit()
        cost = StringMethods.get_unique_digit()

        # Action
        self.add_species(self.species_name)

        purchases_page = PurchasesAllPage(self.driver)
        purchases_page.add_button.click()
        add_dialog = PurchasesAddDialog(self.driver)
        add_dialog.no_boxes.send_keys(no_boxes)
        add_dialog.kg.send_keys(kg)
        add_dialog.cost.send_keys(cost)
        add_dialog.species.select_input_enter(self.species_name)
        add_dialog.save_button.click()

        # Assert
        self.assertEqual(expected_error, add_dialog.error)

        add_dialog.cancel_button.click()

        self.remove_species(self.species_name)

    def test_C140_CheckNoMarketValidation(self):
        # Setup
        expected_error = 'The market_id field is required.'
        no_boxes = StringMethods.get_unique_digit()
        kg = StringMethods.get_unique_digit()
        cost = StringMethods.get_unique_digit()

        # Action
        self.add_species(self.species_name)

        self.add_office(self.office_name)
        self.add_boat(self.boat_name, self.office_name)

        purchases_page = PurchasesAllPage(self.driver)
        purchases_page.add_button.click()
        add_dialog = PurchasesAddDialog(self.driver)
        add_dialog.no_boxes.send_keys(no_boxes)
        add_dialog.kg.send_keys(kg)
        add_dialog.cost.send_keys(cost)
        add_dialog.species.select_input_enter(self.species_name)
        add_dialog.boat.select_input_enter(self.boat_name)
        add_dialog.save_button.click()

        # Assert
        self.assertEqual(expected_error, add_dialog.error)

        add_dialog.cancel_button.click()

        self.remove_species(self.species_name)
        self.remove_boat(self.boat_name)

    def test_C141_CheckNoMarkDoorValidation(self):
        # fails because we cannot add a market
        # Setup
        expected_error = 'The mark_door field is required.'
        no_boxes = StringMethods.get_unique_digit()
        kg = StringMethods.get_unique_digit()
        cost = StringMethods.get_unique_digit()

        # Action
        self.add_species(self.species_name)

        self.add_office(self.office_name)
        self.add_boat(self.boat_name, self.office_name)

        self.add_market(self.market_name,self.number_of_doors)

        purchases_page = PurchasesAllPage(self.driver)
        purchases_page.add_button.click()
        add_dialog = PurchasesAddDialog(self.driver)
        add_dialog.no_boxes.send_keys(no_boxes)
        add_dialog.kg.send_keys(kg)
        add_dialog.cost.send_keys(cost)
        add_dialog.species.select_input_enter(self.species_name)
        add_dialog.boat.select_input_enter(self.boat_name)
        add_dialog.market.select_input_enter(self.market_name)
        add_dialog.market_door.click()
        add_dialog.save_button.click()

        # Assert
        self.assertEqual(expected_error, add_dialog.error)

        add_dialog.cancel_button.click()

        self.remove_market(self.market_name)
        self.remove_species(self.species_name)
        self.remove_boat(self.boat_name)
        self.remove_office(self.office_name)

    def test_C142_CheckIncorrectMarkDoorValidation(self):
        # fails because we cannot add a market and the errror message is not displayed
        # Setup
        expected_error = 'Please enter' # to be completed with the correct error
        no_boxes = StringMethods.get_unique_digit()
        kg = StringMethods.get_unique_digit()
        cost = StringMethods.get_unique_digit()
        mark_door = '@'

        # Action
        self.add_species(self.species_name)

        self.add_office(self.office_name)
        self.add_boat(self.boat_name, self.office_name)

        self.add_market(self.market_name,self.number_of_doors)

        purchases_page = PurchasesAllPage(self.driver)
        purchases_page.add_button.click()
        add_dialog = PurchasesAddDialog(self.driver)
        add_dialog.no_boxes.send_keys(no_boxes)
        add_dialog.kg.send_keys(kg)
        add_dialog.cost.send_keys(cost)
        add_dialog.species.select_input_enter(self.species_name)
        add_dialog.boat.select_input_enter(self.boat_name)
        add_dialog.market.select_input_enter(self.market_name)
        add_dialog.market_door.send_keys(mark_door)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

        self.remove_market(self.market_name)
        self.remove_species(self.species_name)
        self.remove_boat(self.boat_name)
        self.remove_office(self.office_name)




