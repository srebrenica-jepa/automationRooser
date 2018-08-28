#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.TransportsPage import TransportsPage
from TestPages.TestDialogs.TransportsAddDialog import TransportsAddDialog
from TestPages.TestDialogs.TransportsCheckDialog import TransportsCheckDialog
from TestPages.TestDialogs.MessageDialog import MessageDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import CheckOneBox, HeadersTransports


class SmokeTestTransports(BaseTestClass):
    """
    Original implementation - 27/06/2018
    Updates -
    """
    def setUp(self):
        super(SmokeTestTransports, self).setUp()
        self.transports_page = TransportsPage(self.driver)

    def tearDown(self):
        super(SmokeTestTransports, self).tearDown()

    def test_C1_CheckTransportsPageDisplayedCorrectly(self):
        # Setup
        title = 'Transports'
        subtitle = 'Manage transporters (from market to stocks) and shipping companies (delivery to customers).'

        # Assert
        self.assertEqual(title, self.transports_page.title)
        self.assertEqual(subtitle, self.transports_page.subtitle)

    def test_C2_CheckTransportAdded(self):
        # Setup
        transport_name = StringMethods.get_unique_name('transport_name_')
        weight = StringMethods.get_unique_number()
        shipping = CheckOneBox.no

        self.addCleanup(self.transports_page.remove_entry, transport_name)

        # Action
        self.transports_page.add_entry(transport_name, weight, shipping)

        # Assert
        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name)
        self.assertIsNotNone(transport_row)
        self.assertEqual(transport_name, transport_row[HeadersTransports.Name])
        self.assertEqual(weight+' kg', transport_row[HeadersTransports.Weight])

    def test_C3_CheckTransportEdited(self):
        # Setup
        transport_name = StringMethods.get_unique_name('transport_name_')
        weight = StringMethods.get_unique_number()
        shipping = CheckOneBox.no

        # Setup - edit
        transport_name_edited = StringMethods.get_unique_name('transport_name_edited_')
        weight_edited = StringMethods.get_unique_number()
        shipping_edited = CheckOneBox.yes

        self.addCleanup(self.transports_page.remove_entry, transport_name_edited)

        # Action
        self.transports_page.add_entry(transport_name, weight, shipping)
        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name)
        self.transports_page.edit_entry(transport_name_edited, weight_edited, shipping_edited)

        # Assert
        self.transports_page.wait()
        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name_edited)
        self.assertIsNotNone(transport_row)
        self.assertEqual(transport_name_edited, transport_row[HeadersTransports.Name])
        self.assertEqual(weight_edited+' kg', transport_row[HeadersTransports.Weight])

    def test_C4_CheckTransportRemoved(self):
        # Setup
        transport_name = StringMethods.get_unique_name('transport_name_')
        weight = StringMethods.get_unique_number()
        shipping = CheckOneBox.no

        # Action
        self.transports_page.add_entry(transport_name, weight, shipping)
        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name)
        self.transports_page.delete_row(transport_row)

        # Assert
        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name)
        self.assertIsNone(transport_row)

    def test_C9_CheckNewTransportRightDetails(self):
        # Setup
        transport_name = StringMethods.get_unique_name('transport_name_')
        weight = StringMethods.get_unique_number()
        shipping = CheckOneBox.no

        self.addCleanup(self.transports_page.remove_entry, transport_name)

        if shipping==CheckOneBox.no:
            ship="No"
        else:
            ship ="Yes"

        # Action
        self.transports_page.add_entry(transport_name, weight, shipping)

        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name)
        transport_row.details_row_item.click()
        check_dialog = TransportsCheckDialog(self.driver)

        # Assert
        self.assertEqual(transport_name, check_dialog.transport_name)
        self.assertEqual('', check_dialog.delivers)

    def test_C10_CheckTransportDetailsThenEdit(self):
        # Setup
        transport_name = StringMethods.get_unique_name('transport_name_')
        weight = StringMethods.get_unique_number()
        shipping = CheckOneBox.no

        # Setup - edit
        transport_name_edited = StringMethods.get_unique_name('transport_name_edited_')
        weight_edited = StringMethods.get_unique_number()
        shipping_edited = CheckOneBox.yes

        self.addCleanup(self.transports_page.remove_entry, transport_name_edited)

        # Action
        self.transports_page.add_entry(transport_name, weight, shipping)

        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name)
        transport_row.details_row_item.click()
        check_dialog = TransportsCheckDialog(self.driver)
        check_dialog.edit_entry(transport_name_edited, weight_edited, shipping_edited)

        # Assert
        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name_edited)
        self.assertIsNotNone(transport_row)
        self.assertEqual(transport_name_edited, transport_row[HeadersTransports.Name])
        self.assertEqual(weight_edited+' kg', transport_row[HeadersTransports.Weight])

    def test_C11_CheckTransportDetailsThenDelete(self):
        # Setup
        transport_name = StringMethods.get_unique_name('transport_name_')
        weight = StringMethods.get_unique_number()
        shipping = CheckOneBox.no

        # Action
        self.transports_page.add_entry(transport_name, weight, shipping)

        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name)
        transport_row.details_row_item.click()
        check_dialog = TransportsCheckDialog(self.driver)
        check_dialog.remove_entry(transport_name)

        # Assert
        transport_row = self.transports_page.table.get_row_for_field_value(HeadersTransports.Name, transport_name)
        self.assertIsNone(transport_row)

    def test_C5_CheckNoTransportNameValidation(self):
        # Setup
        expected_error = 'This field is required'

        # Action
        self.transports_page.add_button.click()
        add_dialog = TransportsAddDialog(self.driver)
        add_dialog.name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C8_CheckIncorrectTransportNameValidation(self):
        # Setup
        transport_name = '@'
        expected_error = 'Please enter a name with 3-30 characters'

        # Action
        self.transports_page.add_button.click()
        add_dialog = TransportsAddDialog(self.driver)
        add_dialog.name.send_keys(transport_name)
        add_dialog.minimum_weight.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C6_CheckIncorrecMinWeightValidation(self):
        # Setup
        weight = '-2'
        expected_error = 'Please enter a value greater than or equal to 0'

        # Action
        self.transports_page.add_button.click()
        add_dialog = TransportsAddDialog(self.driver)
        add_dialog.minimum_weight.send_keys(weight)
        add_dialog.name.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C105_CheckNoDuplicateEntriesAllowed(self):
        # Setup
        transport_name = StringMethods.get_unique_name('transport_name_')
        weight = StringMethods.get_unique_number()
        shipping = CheckOneBox.no

        error_message = 'Duplicate entries are not allowed.'

        # Action
        self.transports_page.add_entry(transport_name, weight, shipping)
        transports_page = TransportsPage(self.driver)
        transports_page.add_entry(transport_name, weight, shipping)
        message_dialog = MessageDialog(self.driver)
        message_dialog.wait()

        # Assert
        self.assertTrue(error_message, message_dialog.get_inner_text())

        self.transports_page.remove_entry(transport_name)
