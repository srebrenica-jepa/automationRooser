#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.SpeciesPage import SpeciesPage
from TestPages.TestDialogs.SpeciesAddDialog import SpeciesAddDialog
from TestPages.TestDialogs.MessageDialog import MessageDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import TableHeaders


class SmokeTestSpecies(BaseTestClass):
    def setUp(self):
        super(SmokeTestSpecies, self).setUp()
        self.species_page = SpeciesPage(self.driver)

    def tearDown(self):
        super(SmokeTestSpecies, self).tearDown()

    def test_C54_CheckSpeciesPageDisplayedCorrectly(self):
        # Setup
        title = 'Species'
        subtitle = 'Manage species bought at the market.'

        # Assert
        self.assertEqual(title, self.species_page.title)
        self.assertEqual(subtitle, self.species_page.subtitle)

    def test_C55_CheckSpeciesAdded(self):
        # Setup
        species_name = StringMethods.get_unique_name('species_name_')

        self.addCleanup(self.species_page.remove_entry, species_name)

        # Action
        self.species_page.add_entry(species_name)

        # Assert
        species_row = self.species_page.table.get_row_for_field_value(TableHeaders.Name, species_name)
        self.assertIsNotNone(species_row)
        self.assertEqual(species_name, species_row[TableHeaders.Name])

    def test_C56_CheckSpeciesEdited(self):
        # Setup
        species_name = StringMethods.get_unique_name('species_name_')

        # Setup - edit
        species_name_edited = StringMethods.get_unique_name('species_name_edited_')

        self.addCleanup(self.species_page.remove_entry, species_name_edited)

        # Action
        self.species_page.add_entry(species_name)
        species_row = self.species_page.table.get_row_for_field_value(TableHeaders.Name, species_name)
        self.species_page.edit_entry(species_row, species_name_edited)

        # Assert
        self.species_page.wait_for_page()
        species_row = self.species_page.table.get_row_for_field_value(TableHeaders.Name, species_name_edited)
        self.assertIsNotNone(species_row)
        self.assertEqual(species_name_edited, species_row[TableHeaders.Name])

    def test_C57_CheckSpeciesRemoved(self):
        # Setup
        no_species_message = 'There is no data to display'
        species_name = StringMethods.get_unique_name('species_name_')

        # Action
        self.species_page.add_entry(species_name)
        species_row = self.species_page.table.get_row_for_field_value(TableHeaders.Name, species_name)
        self.species_page.delete_row(species_row)

        # Assert
        self.assertEqual(no_species_message, self.species_page.empty_text)

    def test_C58_CheckNoSpeciesNameValidation(self):
        # Setup
        expected_error = 'Species name is required'

        # Action
        self.species_page.add_button.click()
        add_dialog = SpeciesAddDialog(self.driver)
        add_dialog.name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C59_CheckIncorrectSpeciesNameValidation(self):
        # Setup
        species_name = '@'
        expected_error = 'Please enter at least 5 characters'

        # Action
        self.species_page.add_button.click()
        add_dialog = SpeciesAddDialog(self.driver)
        add_dialog.name.send_keys(species_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C110_CheckNoDuplicateEntriesAllowed(self):
        # Setup
        species_name = StringMethods.get_unique_name('species_name_')

        expected_error = 'Duplicate entries are not allowed.'

        # Action
        self.species_page.add_entry(species_name)
        species_page = SpeciesPage(self.driver)
        species_page.add_button.click()
        add_dialog = SpeciesAddDialog(self.driver)
        add_dialog.name.send_keys(species_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()
        species_page.remove_entry(species_name)
