#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.OfficesPage import OfficesPage
from TestPages.TestDialogs.OfficesAddDialog import OfficesAddDialog
from TestPages.TestDialogs.OfficesCheckDialog import OfficesCheckDialog
from TestPages.TestDialogs.MessageDialog import MessageDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import TableHeaders


class SmokeTestOffices(BaseTestClass):
    def setUp(self):
        super(SmokeTestOffices, self).setUp()
        self.offices_page = OfficesPage(self.driver)

    def tearDown(self):
        super(SmokeTestOffices, self).tearDown()

    def test_C24_CheckOfficesPageDisplayedCorrectly(self):
        # Setup
        title = 'Offices'
        subtitle = 'Manage offices and their preferences.'

        # Assert
        self.assertEqual(title, self.offices_page.title)
        self.assertEqual(subtitle, self.offices_page.subtitle)

    def test_C25_CheckOfficeAdded(self):
        # Setup
        office_name = StringMethods.get_unique_name('office_name_')

        self.addCleanup(self.offices_page.remove_entry, office_name)

        # Action
        self.offices_page.add_entry(office_name)

        # Assert
        office_row = self.offices_page.table.get_row_for_field_value(TableHeaders.Name, office_name)
        self.assertIsNotNone(office_row)
        self.assertEqual(office_name, office_row[TableHeaders.Name])

    def test_C26_CheckOfficeEdited(self):
        # Setup
        office_name = StringMethods.get_unique_name('office_name_')

        # Setup - edit
        office_name_edited = StringMethods.get_unique_name('office_name_edited_')

        self.addCleanup(self.offices_page.remove_entry, office_name_edited)

        # Action
        self.offices_page.add_entry(office_name)
        office_row = self.offices_page.table.get_row_for_field_value(TableHeaders.Name, office_name)
        self.offices_page.edit_entry(office_row, office_name_edited)

        # Assert
        self.offices_page.wait_for_page()
        office_row = self.offices_page.table.get_row_for_field_value(TableHeaders.Name, office_name_edited)
        self.assertIsNotNone(office_row)
        self.assertEqual(office_name_edited, office_row[TableHeaders.Name])

    def test_C27_CheckOfficeRemoved(self):
        # Setup
        no_office_message = 'There is no data to display'
        office_name = StringMethods.get_unique_name('office_name_')

        # Action
        self.offices_page.add_entry(office_name)
        office_row = self.offices_page.table.get_row_for_field_value(TableHeaders.Name, office_name)
        self.offices_page.delete_row(office_row)

        # Assert
        self.assertEqual(no_office_message, self.offices_page.empty_text)

    def test_C28_CheckNewOfficeRightDetails(self):
        # Setup
        office_name = StringMethods.get_unique_name('office_name_')

        # Action
        self.offices_page.add_entry(office_name)
        office_row = self.offices_page.table.get_row_for_field_value(TableHeaders.Name, office_name)
        office_row.details_row_item.click()
        check_dialog = OfficesCheckDialog(self.driver)

        # Assert
        self.assertEqual(office_name, check_dialog.office_name)

        check_dialog.remove_entry(office_name)

    def test_C29_CheckOfficeDetailsThenEdit(self):
        # Setup
        office_name = StringMethods.get_unique_name('office_name_')

        # Setup - edit
        office_name_edited = StringMethods.get_unique_name('office_name_edited_')

        self.addCleanup(self.offices_page.remove_entry, office_name_edited)

        # Action
        self.offices_page.add_entry(office_name)

        office_row = self.offices_page.table.get_row_for_field_value(TableHeaders.Name, office_name)
        office_row.details_row_item.click()
        check_dialog = OfficesCheckDialog(self.driver)
        check_dialog.edit_entry(office_name_edited)

        # Assert
        office_row = self.offices_page.table.get_row_for_field_value(TableHeaders.Name, office_name_edited)
        self.assertIsNotNone(office_row)
        self.assertEqual(office_name_edited, office_row[TableHeaders.Name])

    def test_C30_CheckOfficeDetailsThenDelete(self):
        # Setup
        no_office_message = 'There is no data to display'
        office_name = StringMethods.get_unique_name('office_name_')

        # Action
        self.offices_page.add_entry(office_name)

        office_row = self.offices_page.table.get_row_for_field_value(TableHeaders.Name, office_name)
        office_row.details_row_item.click()
        check_dialog = OfficesCheckDialog(self.driver)
        check_dialog.remove_entry(office_name)

        # Assert
        self.assertEqual(no_office_message, self.offices_page.empty_text)

    def test_C31_CheckNoOfficeNameValidation(self):
        # Setup
        expected_error = 'This field is required'

        # Action
        self.offices_page.add_button.click()
        add_dialog = OfficesAddDialog(self.driver)
        add_dialog.name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C32_CheckIncorrectOfficeNameValidation(self):
        # Setup
        office_name = '@'
        expected_error = 'Please enter a name of at least 3 characters'

        # Action
        self.offices_page.add_button.click()
        add_dialog = OfficesAddDialog(self.driver)
        add_dialog.name.send_keys(office_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C108_CheckNoDuplicateEntriesAllowed(self):
        # Setup
        office_name = StringMethods.get_unique_name('office_name_')

        expected_error = 'Duplicate entries are not allowed.'

        # Action
        self.offices_page.add_entry(office_name)
        offices_page = OfficesPage(self.driver)
        offices_page.add_button.click()
        add_dialog = OfficesAddDialog(self.driver)
        add_dialog.name.send_keys(office_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()
        offices_page.remove_entry(office_name)
