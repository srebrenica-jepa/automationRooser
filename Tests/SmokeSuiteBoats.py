#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.OfficesPage import OfficesPage
from TestPages.BoatsPage import BoatsPage
from TestPages.TestDialogs.BoatsAddDialog import BoatsAddDialog
from TestPages.TestDialogs.BoatsCheckDialog import BoatsCheckDialog
from TestPages.TestDialogs.MessageDialog import MessageDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import HeadersBoats


class SmokeTestBoats(BaseTestClass):
    def setUp(self):
        super(SmokeTestBoats, self).setUp()
        self.boats_page = BoatsPage(self.driver)
        self.office_name = StringMethods.get_unique_name('office_name_')

    def tearDown(self):
        super(SmokeTestBoats, self).tearDown()

    def add_office(self, office_name):
        office_page = OfficesPage(self.driver)
        office_page.add_entry(office_name)

    def remove_office(self, office_name):
        office_page = OfficesPage(self.driver)
        office_page.remove_entry(office_name)

    def test_C33_CheckBoatsPageDisplayedCorrectly(self):
        # Setup
        title = 'Boats'
        subtitle = 'Manage boats and their preferences.'

        # Assert
        self.assertEqual(title, self.boats_page.title)
        self.assertEqual(subtitle, self.boats_page.subtitle)

    def test_C34_CheckBoatAdded(self):
        # Setup
        boat_name = StringMethods.get_unique_name('boat_name_')
        self.add_office(self.office_name)

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_entry(boat_name, self.office_name)

        # Assert
        boat_row = boats_page.table.get_row_for_field_value(HeadersBoats.Name, boat_name)
        self.assertIsNotNone(boat_row)
        self.assertEqual(boat_name, boat_row[HeadersBoats.Name])
        self.assertEqual(self.office_name, boat_row[HeadersBoats.Supplier])

        boats_page.remove_entry(boat_name)
        self.remove_office(self.office_name)

    def test_C35_CheckBoatEdited(self):
        # Setup
        boat_name = StringMethods.get_unique_name('boat_name_')
        self.add_office(self.office_name)

        # Setup - edit
        boat_name_edited = StringMethods.get_unique_name('boat_name_edited_')

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_entry(boat_name, self.office_name)
        boat_row = boats_page.table.get_row_for_field_value(HeadersBoats.Name, boat_name)
        boats_page.edit_entry(boat_row, boat_name_edited, self.office_name)

        # Assert
        boats_page = BoatsPage(self.driver)
        boat_row = boats_page.table.get_row_for_field_value(HeadersBoats.Name, boat_name_edited)
        self.assertIsNotNone(boat_row)
        self.assertEqual(boat_name_edited, boat_row[HeadersBoats.Name])
        self.assertEqual(self.office_name, boat_row[HeadersBoats.Supplier])

        boats_page.remove_entry(boat_name_edited)
        self.remove_office(self.office_name)

    def test_C36_CheckBoatRemoved(self):
        # Setup
        no_boat_message = 'There is no data to display'
        boat_name = StringMethods.get_unique_name('boat_name_')
        self.add_office(self.office_name)

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_entry(boat_name, self.office_name)
        boat_row = boats_page.table.get_row_for_field_value(HeadersBoats.Name, boat_name)
        boats_page.delete_row(boat_row)

        # Assert
        self.assertEqual(no_boat_message, boats_page.empty_text)

        self.remove_office(self.office_name)

    def test_C37_CheckNewBoatRightDetails(self):
        # Setup
        boat_name = StringMethods.get_unique_name('boat_name_')
        self.add_office(self.office_name)

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_entry(boat_name, self.office_name)

        # Action
        boat_row = boats_page.table.get_row_for_field_value(HeadersBoats.Name, boat_name)
        boat_row.details_row_item.click()
        check_dialog = BoatsCheckDialog(self.driver)

        # Assert
        self.assertEqual(boat_name, check_dialog.boat_name)
        self.assertEqual(self.office_name, check_dialog.supplier)

        check_dialog.remove_entry(boat_name)
        self.remove_office(self.office_name)

    def test_C38_CheckBoatDetailsThenEdit(self):
        # Setup
        boat_name = StringMethods.get_unique_name('boat_name_')
        self.add_office(self.office_name)

        # Setup - edit
        boat_name_edited = StringMethods.get_unique_name('boat_name_edited_')

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_entry(boat_name, self.office_name)

        boat_row = boats_page.table.get_row_for_field_value(HeadersBoats.Name, boat_name)
        boat_row.details_row_item.click()
        check_dialog = BoatsCheckDialog(self.driver)
        check_dialog.edit_entry(boat_name_edited, self.office_name)

        # Assert
        boat_row = boats_page.table.get_row_for_field_value(HeadersBoats.Name, boat_name_edited)
        self.assertIsNotNone(boat_row)
        self.assertEqual(boat_name_edited, boat_row[HeadersBoats.Name])
        self.assertEqual(self.office_name, boat_row[HeadersBoats.Supplier])

        boats_page.remove_entry(boat_name_edited)
        self.remove_office(self.office_name)

    def test_C39_CheckBoatDetailsThenDelete(self):
        # Setup
        no_boat_message = 'There is no data to display'
        boat_name = StringMethods.get_unique_name('boat_name_')
        self.add_office(self.office_name)

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_entry(boat_name, self.office_name)

        boat_row = boats_page.table.get_row_for_field_value(HeadersBoats.Name, boat_name)
        boat_row.details_row_item.click()
        check_dialog = BoatsCheckDialog(self.driver)
        check_dialog.remove_entry(boat_name)

        # Assert
        self.assertEqual(no_boat_message, boats_page.empty_text)

        self.remove_office(self.office_name)

    def test_C40_CheckNoBoatNameValidation(self):
        # Setup
        expected_error = 'Boat name is required'

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_button.click()
        add_dialog = BoatsAddDialog(self.driver)
        add_dialog.name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C41_CheckIncorrectBoatNameValidation(self):
        # Setup
        boat_name = '@'
        expected_error = 'Please enter a name of at least 3 characters'

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_button.click()
        add_dialog = BoatsAddDialog(self.driver)
        add_dialog.name.send_keys(boat_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C42_CheckNoOfficeValidation(self):
        # Setup
        boat_name = StringMethods.get_unique_name('boat_name_')
        expected_error = 'This field is required'

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_button.click()
        add_dialog = BoatsAddDialog(self.driver)
        add_dialog.name.send_keys(boat_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C109_CheckNoDuplicateEntriesAllowed(self):
        # Setup
        expected_error = 'Duplicate entries are not allowed.'
        boat_name = StringMethods.get_unique_name('boat_name_')
        self.add_office(self.office_name)

        # Action
        boats_page = BoatsPage(self.driver)
        boats_page.add_entry(boat_name, self.office_name)

        boats_page = BoatsPage(self.driver)
        boats_page.add_button.click()
        add_dialog = BoatsAddDialog(self.driver)
        add_dialog.name.send_keys(boat_name)
        add_dialog.office.select_input(self.office_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()
        boats_page.remove_entry(boat_name)
        self.remove_office(self.office_name)
