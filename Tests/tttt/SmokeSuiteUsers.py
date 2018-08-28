#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.UsersPage import UsersPage
from TestPages.MarketsPage import MarketsPage
from TestPages.TestDialogs.UsersAddDialog import UsersAddDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import HeadersUsers, UserRole


class SmokeTestUsers(BaseTestClass):
    def setUp(self):
        super(SmokeTestUsers, self).setUp()
        self.users_page = UsersPage(self.driver)
        self.market_name = StringMethods.get_unique_name('market_name_')
        self.number_of_doors = StringMethods.get_unique_number()

    def tearDown(self):
        super(SmokeTestUsers, self).tearDown()

    def add_market(self, market_name, number_of_doors):
        market_page = MarketsPage(self.driver)
        market_page.add_entry(market_name, number_of_doors)

    def remove_market(self, market_name):
        market_page = MarketsPage(self.driver)
        market_page.remove_entry(market_name)

    def test_C94_CheckUsersPageDisplayedCorrectly(self):
        # Setup
        title = 'Users'
        subtitle = 'Manage users access to Rooser (mobile and web) and their roles.'

        # Assert
        self.assertEqual(title, self.users_page.title)
        self.assertEqual(subtitle, self.users_page.subtitle)

    def test_C95_CheckUserNotPaletterAdded(self):
        # Setup
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = StringMethods.get_unique_email()
        password = StringMethods.get_unique_password()
        role = UserRole.Buyer

        self.addCleanup(self.users_page.remove_entry, first_name)

        # Action
        self.users_page.add_entry(first_name, last_name, email, password, role)

        # Assert
        user_row = self.users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name)
        self.assertIsNotNone(user_row)
        self.assertEqual(first_name, user_row[HeadersUsers.FirstName])
        self.assertEqual(last_name, user_row[HeadersUsers.LastName])
        self.assertEqual(email, user_row[HeadersUsers.Email])
        self.assertEqual(role, user_row[HeadersUsers.Role])

    def test_C96_CheckUserNotPaletterEdited(self):
        # Setup
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = StringMethods.get_unique_email()
        password = StringMethods.get_unique_password()
        role = UserRole.Buyer

        # Setup - edit
        first_name_edited = StringMethods.get_unique_name('first_name_edited_')
        last_name_edited = StringMethods.get_unique_name('last_name_edited_')
        email_edited = StringMethods.get_unique_email()
        password_edited = StringMethods.get_unique_password()
        role_edited = UserRole.Manager

        self.addCleanup(self.users_page.remove_entry, first_name_edited)

        # Action
        self.users_page.add_entry(first_name, last_name, email, password, role)
        user_row = self.users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name)
        self.users_page.edit_entry(user_row, first_name_edited, last_name_edited, email_edited, password_edited, role_edited)

        # Assert
        self.users_page.wait_for_page()
        user_row = self.users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name_edited)
        self.assertIsNotNone(user_row)
        self.assertEqual(first_name_edited, user_row[HeadersUsers.FirstName])

    def test_C97_CheckUserNotPaletterRemoved(self):
        # Setup
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = StringMethods.get_unique_email()
        password = StringMethods.get_unique_password()
        role = UserRole.Buyer

        # Action
        self.users_page.add_entry(first_name, last_name, email, password, role)
        user_row = self.users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name)
        self.users_page.delete_row(user_row)
        user_row = self.users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name)

        # Assert
        self.assertIsNone(user_row)

    def test_C121_CheckUserPaletterAdded(self):
        # fails because a market cannot be added
        # Setup
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = StringMethods.get_unique_email()
        password = StringMethods.get_unique_password()
        role = UserRole.Paletter

        self.addCleanup(self.users_page.remove_entry, first_name)

        # Action
        self.add_market(self.market_name, self.number_of_doors)
        users_page = UsersPage(self.driver)
        users_page.add_entry(first_name, last_name, email, password, role)

        # Assert
        user_row = users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name)
        self.assertIsNotNone(user_row)
        self.assertEqual(first_name, user_row[HeadersUsers.FirstName])
        self.assertEqual(last_name, user_row[HeadersUsers.LastName])
        self.assertEqual(email, user_row[HeadersUsers.Email])
        self.assertEqual(role, user_row[HeadersUsers.Role])

        self.remove_market(self.market_name)

    def test_C122_CheckUserPaletterEdited(self):
        # fails because a market cannot be added
        # Setup
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = StringMethods.get_unique_email()
        password = StringMethods.get_unique_password()
        role = UserRole.Paletter

        # Setup - edit
        first_name_edited = StringMethods.get_unique_name('first_name_edited_')
        last_name_edited = StringMethods.get_unique_name('last_name_edited_')
        email_edited = StringMethods.get_unique_email()
        password_edited = StringMethods.get_unique_password()
        role_edited = UserRole.Manager

        self.addCleanup(self.users_page.remove_entry, first_name_edited)

        # Action
        self.add_market(self.market_name, self.number_of_doors)
        users_page = UsersPage(self.driver)
        users_page.add_entry(first_name, last_name, email, password, role)
        user_row = users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name)
        users_page.edit_entry(user_row, first_name_edited, last_name_edited, email_edited, password_edited, role_edited)

        # Assert
        user_row = users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name_edited)
        self.assertIsNotNone(user_row)
        self.assertEqual(first_name_edited, user_row[HeadersUsers.FirstName])

        self.remove_market(self.market_name)

    def test_C123_CheckUserPaletterRemoved(self):
        # fails because a market cannot be added
        # Setup
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = StringMethods.get_unique_email()
        password = StringMethods.get_unique_password()
        role = UserRole.Paletter

        # Action
        self.add_market(self.market_name, self.number_of_doors)
        users_page = UsersPage(self.driver)
        users_page.add_entry(first_name, last_name, email, password, role)
        user_row = users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name)
        users_page.delete_row(user_row)
        user_row = users_page.table.get_row_for_field_value(HeadersUsers.FirstName, first_name)

        # Assert
        self.assertIsNone(user_row)

        self.remove_market(self.market_name)

    def test_C98_CheckNoFirstNameValidation(self):
        # Setup
        expected_error = 'First name is required'

        # Action
        self.users_page.add_button.click()
        add_dialog = UsersAddDialog(self.driver)
        add_dialog.first_name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C99_CheckIncorrectFirstNameValidation(self):
        # Setup
        first_name = '@'
        expected_error = 'Please enter between 2-20 characters'

        # Action
        self.users_page.add_button.click()
        add_dialog = UsersAddDialog(self.driver)
        add_dialog.first_name.send_keys(first_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C100_CheckNoLastNameValidation(self):
        # Setup
        expected_error = 'Last name is required'
        first_name = StringMethods.get_unique_name('first_name_')

        # Action
        self.users_page.add_button.click()
        add_dialog = UsersAddDialog(self.driver)
        add_dialog.first_name.send_keys(first_name)
        add_dialog.last_name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C101_CheckIncorrectLastNameValidation(self):
        # Setup
        expected_error = 'Please enter between 2-20 characters'
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = '@'

        # Action
        self.users_page.add_button.click()
        add_dialog = UsersAddDialog(self.driver)
        add_dialog.first_name.send_keys(first_name)
        add_dialog.last_name.send_keys(last_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C102_CheckNoEmailValidation(self):
        # Setup
        expected_error = 'Email address is needed'
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')

        # Action
        self.users_page.add_button.click()
        add_dialog = UsersAddDialog(self.driver)
        add_dialog.first_name.send_keys(first_name)
        add_dialog.last_name.send_keys(last_name)
        add_dialog.email.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C120_CheckIncorrectEmailValidation(self):
        # Setup
        expected_error = 'EMAIL MUST FOLLOW FORMAT: ANY@ANY.ANY'
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = '@'

        # Action
        self.users_page.add_button.click()
        add_dialog = UsersAddDialog(self.driver)
        add_dialog.first_name.send_keys(first_name)
        add_dialog.last_name.send_keys(last_name)
        add_dialog.email.send_keys(email)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C103_CheckNoPasswordValidation(self):
        # Setup
        expected_error = 'A password is needed'
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = StringMethods.get_unique_email()

        # Action
        self.users_page.add_button.click()
        add_dialog = UsersAddDialog(self.driver)
        add_dialog.first_name.send_keys(first_name)
        add_dialog.last_name.send_keys(last_name)
        add_dialog.email.send_keys(email)
        add_dialog.password.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C104_CheckIncorrectPaswordValidation(self):
        # Setup
        expected_error = 'THE PASSWORD MUST BE AT LEAST 6 CHARACTERS LONG.'
        first_name = StringMethods.get_unique_name('first_name_')
        last_name = StringMethods.get_unique_name('last_name_')
        email = StringMethods.get_unique_email()
        password = '@'

        # Action
        self.users_page.add_button.click()
        add_dialog = UsersAddDialog(self.driver)
        add_dialog.first_name.send_keys(first_name)
        add_dialog.last_name.send_keys(last_name)
        add_dialog.email.send_keys(email)
        add_dialog.password.send_keys(password)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

