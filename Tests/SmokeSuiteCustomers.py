#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.CustomersPage import CustomersPage
from TestPages.TransportsPage import TransportsPage
from TestPages.TestDialogs.CustomersAddDialog import CustomersAddDialog
from TestPages.TestDialogs.CustomersEditDialog import CustomersEditDialog
from TestPages.TestDialogs.CustomersCheckDialog import CustomersCheckDialog
from TestPages.TestDialogs.MessageDialog import MessageDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import HeadersCustomers, Currency, Weight, CheckOneBox


class SmokeTestCustomers(BaseTestClass):
    def setUp(self):
        super(SmokeTestCustomers, self).setUp()
        self.customers_page = CustomersPage(self.driver)

        self.transport_name = StringMethods.get_unique_name('transport_name_')

    def tearDown(self):
        super(SmokeTestCustomers, self).tearDown()

    def add_transport(self, transport_name, weight=None, shipping=CheckOneBox.no):
        transport_page = TransportsPage(self.driver)
        transport_page.add_entry(transport_name, weight, shipping)

    def remove_transport(self, transport_name):
        transport_page = TransportsPage(self.driver)
        transport_page.remove_entry(transport_name)

    def test_C43_CheckCustomersPageDisplayedCorrectly(self):
        # Setup
        title = 'Customers'
        subtitle = 'Manage customers and their preferences.'

        # Assert
        self.assertEqual(title, self.customers_page.title)
        self.assertEqual(subtitle, self.customers_page.subtitle)

    def test_C44_CheckCustomerAdded(self):
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene=False

        self.addCleanup(self.customers_page.remove_entry, customer_name)

        # Action
        self.customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)

        # Assert
        customer_row = self.customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        self.assertIsNotNone(customer_row)
        self.assertEqual(customer_name, customer_row[HeadersCustomers.Name])
        self.assertEqual(sage_code, customer_row[HeadersCustomers.SageCode])

    def test_C45_CheckCustomerEdited(self):
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Setup - edit
        customer_name_edited = StringMethods.get_unique_name('customer_name_edited_')
        sage_code_edited = StringMethods.get_unique_name('sage_edited_')
        display_edited = StringMethods.get_unique_name('display_edited_')
        transport_edited = None
        currency_edited = Currency.Dollar
        weight_edited = Weight.St
        hygiene_edited = True

        self.addCleanup(self.customers_page.remove_entry, customer_name_edited)

        # Action
        self.customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customer_row = self.customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        self.customers_page.edit_entry(customer_row, customer_name_edited,
        sage_code_edited, display_edited, transport_edited, currency_edited, weight_edited, hygiene_edited)

        # Assert
        self.customers_page.wait_for_page()
        customer_row = self.customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name_edited)
        self.assertIsNotNone(customer_row)
        self.assertEqual(customer_name_edited, customer_row[HeadersCustomers.Name])
        self.assertEqual(sage_code_edited, customer_row[HeadersCustomers.SageCode])

    def test_C46_CheckCustomerRemoved(self):
        # Setup
        no_customer_message = 'There is no data to display'
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Action
        self.customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customer_row = self.customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        self.customers_page.delete_row(customer_row)

        # Assert
        self.assertEqual(no_customer_message, self.customers_page.empty_text)

    def test_C47_CheckNewCustomerRightDetails(self):
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Action
        self.customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customer_row = self.customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        customer_row.details_row_item.click()
        check_dialog = CustomersCheckDialog(self.driver)

        # Assert
        self.assertEqual(customer_name, check_dialog.customer_name)

        check_dialog.remove_entry(customer_name)

    def test_C48_CheckCustomerDetailsThenEdit(self):
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Setup - edit
        customer_name_edited = StringMethods.get_unique_name('customer_name_edited_')
        sage_code_edited = StringMethods.get_unique_name('sage_edited_')
        display_edited = StringMethods.get_unique_name('display_edited_')
        transport_edited = None
        currency_edited = Currency.Dollar
        weight_edited = Weight.St
        hygiene_edited = True

        self.addCleanup(self.customers_page.remove_entry, customer_name_edited)

        # Action
        self.customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customer_row = self.customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        customer_row.details_row_item.click()
        check_dialog = CustomersCheckDialog(self.driver)
        check_dialog.edit_entry(customer_name_edited, sage_code_edited, display_edited, transport_edited,
                                currency_edited, weight_edited, hygiene_edited)

        # Assert
        customer_row = self.customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name_edited)
        self.assertIsNotNone(customer_row)
        self.assertEqual(customer_name_edited, customer_row[HeadersCustomers.Name])

    def test_C49_CheckCustomerDetailsThenDelete(self):
        # Setup
        no_customers_message = 'There is no data to display'
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Action
        self.customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)

        customer_row = self.customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        customer_row.details_row_item.click()
        check_dialog = CustomersCheckDialog(self.driver)
        check_dialog.remove_entry(customer_name)

        # Assert
        self.assertEqual(no_customers_message, self.customers_page.empty_text)

    def test_C50_CheckNoCustomerNameValidation(self):
        # Setup
        expected_error = 'Business name is required'

        # Action
        self.customers_page.add_button.click()
        add_dialog = CustomersAddDialog(self.driver)
        add_dialog.name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C51_CheckIncorrectCustomerNameValidation(self):
        # Setup
        customer_name = '@'
        expected_error = 'Please enter a name of at least 3 characters'

        # Action
        self.customers_page.add_button.click()
        add_dialog = CustomersAddDialog(self.driver)
        add_dialog.name.send_keys(customer_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C52_CheckNoSageCodeValidation(self):
        # Setup
        expected_error = 'THE SAGE CODE IS REQUIRED'
        customer_name = StringMethods.get_unique_name('customer_name_')

        # Action
        self.customers_page.add_button.click()
        add_dialog = CustomersAddDialog(self.driver)
        add_dialog.name.send_keys(customer_name)
        add_dialog.sage.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C53_CheckIncorrectSageCodeValidation(self):
        # Setup
        sage_code= '@'
        customer_name = StringMethods.get_unique_name('customer_name_')
        expected_error = 'THE SAGE CODE IS REQUIRED'

        # Action
        self.customers_page.add_button.click()
        add_dialog = CustomersAddDialog(self.driver)
        add_dialog.name.send_keys(customer_name)
        add_dialog.sage.send_keys(sage_code)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C111_CheckCustomerWithTransportAdded(self):
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene=False

        # Action
        self.add_transport(self.transport_name)
        customers_page = CustomersPage(self.driver)
        customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)

        # Assert
        customers_page = CustomersPage(self.driver)
        customer_row = customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        self.assertIsNotNone(customer_row)
        self.assertEqual(customer_name, customer_row[HeadersCustomers.Name])
        self.assertEqual(sage_code, customer_row[HeadersCustomers.SageCode])

        customers_page.delete_row(customer_row)

        self.remove_transport(self.transport_name)

    def test_C112_CheckCustomerWithTransportEdited(self):
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Setup - edit
        customer_name_edited = StringMethods.get_unique_name('customer_name_edited_')
        sage_code_edited = StringMethods.get_unique_name('sage_edited_')
        display_edited = StringMethods.get_unique_name('display_edited_')
        transport_edited = None
        currency_edited = Currency.Dollar
        weight_edited = Weight.St
        hygiene_edited = True

        # Action
        self.add_transport(self.transport_name)
        customers_page = CustomersPage(self.driver)
        customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customer_row = customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        customers_page.edit_entry(customer_row, customer_name_edited,
                                  sage_code_edited, display_edited, transport_edited, currency_edited, weight_edited, hygiene_edited)

        # Assert
        customers_page = CustomersPage(self.driver)
        customer_row = customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name_edited)
        self.assertIsNotNone(customer_row)
        self.assertEqual(customer_name_edited, customer_row[HeadersCustomers.Name])
        self.assertEqual(sage_code_edited, customer_row[HeadersCustomers.SageCode])

        customers_page.delete_row(customer_row)

        self.remove_transport(self.transport_name)

    def test_C113_CheckCustomerWithTransportRemoved(self):
        # Setup
        no_customer_message = 'There is no data to display'
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Action
        self.add_transport(self.transport_name)
        customers_page = CustomersPage(self.driver)
        customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customers_page = CustomersPage(self.driver)
        customer_row = customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        customers_page.delete_row(customer_row)

        # Assert
        self.assertEqual(no_customer_message, customers_page.empty_text)

        self.remove_transport(self.transport_name)

    def test_C114_CheckNewCustomerWithTransportRightDetails(self):
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Action
        self.add_transport(self.transport_name)
        customers_page = CustomersPage(self.driver)
        customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customers_page = CustomersPage(self.driver)
        customer_row = customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        customer_row.details_row_item.click()
        check_dialog = CustomersCheckDialog(self.driver)

        # Assert
        self.assertEqual(customer_name, check_dialog.customer_name)

        check_dialog.remove_entry(customer_name)

        self.remove_transport(self.transport_name)

    def test_C115_CheckCustomerWithTransportDetailsThenEdit(self):
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Setup - edit
        customer_name_edited = StringMethods.get_unique_name('customer_name_edited_')
        sage_code_edited = StringMethods.get_unique_name('sage_edited_')
        display_edited = StringMethods.get_unique_name('display_edited_')
        transport_edited = None
        currency_edited = Currency.Dollar
        weight_edited = Weight.St
        hygiene_edited = True

        self.addCleanup(self.customers_page.remove_entry, customer_name_edited)

        # Action
        self.add_transport(self.transport_name)
        customers_page = CustomersPage(self.driver)
        customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customers_page = CustomersPage(self.driver)
        customer_row = customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        customer_row.details_row_item.click()
        check_dialog = CustomersCheckDialog(self.driver)
        check_dialog.edit_entry(customer_name_edited, sage_code_edited, display_edited, transport_edited,
                                currency_edited, weight_edited, hygiene_edited)

        # Assert
        customers_page = CustomersPage(self.driver)
        customers_page.wait_for_page()
        customer_row = customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name_edited)
        self.assertIsNotNone(customer_row)
        self.assertEqual(customer_name_edited, customer_row[HeadersCustomers.Name])

        customers_page.delete_row(customer_row)

        self.remove_transport(self.transport_name)

    def test_C116_CheckCustomerWithTransportDetailsThenDelete(self):
        # Setup
        no_customers_message = 'There is no data to display'
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        # Action
        self.add_transport(self.transport_name)
        customers_page = CustomersPage(self.driver)
        customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        customers_page = CustomersPage(self.driver)
        customer_row = customers_page.table.get_row_for_field_value(HeadersCustomers.Name, customer_name)
        customer_row.details_row_item.click()
        check_dialog = CustomersCheckDialog(self.driver)
        check_dialog.remove_entry(customer_name)

        # Assert
        self.assertEqual(no_customers_message, customers_page.empty_text)

        self.remove_transport(self.transport_name)

    def test_C117_CheckNoDuplicateEntriesAllowed(self):
        # fails because duplication is allowed
        # Setup
        customer_name = StringMethods.get_unique_name('customer_name_')
        sage_code = StringMethods.get_unique_name('sage_')
        display = StringMethods.get_unique_name('display_')
        transport = None
        currency = Currency.Pound
        weight = Weight.Kg
        hygiene = False

        expected_error = 'Duplicate entries are not allowed.'

        # Action
        self.add_transport(self.transport_name)
        customers_page = CustomersPage(self.driver)
        customers_page.add_entry(customer_name, sage_code, display, transport, currency, weight, hygiene)
        confirmation_dialog = ConfirmationMessageDialog(self.driver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Customer created.')
        customers_page = CustomersPage(self.driver)
        customers_page.add_button.click()
        add_dialog = CustomersAddDialog(self.driver)
        add_dialog.name.send_keys(customer_name)
        add_dialog.sage.send_keys(sage_code)
        add_dialog.display.send_keys(display)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()
        customers_page.remove_entry(customer_name)
