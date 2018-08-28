#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.ProductsPage import ProductsPage
from TestPages.TestDialogs.ProductsAddDialog import ProductsAddDialog
from TestPages.TestDialogs.ProductsCheckDialog import ProductsCheckDialog
from TestPages.TestDialogs.ConfirmationMessageDialog import ConfirmationMessageDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import HeadersProducts, DefaultCut


class SmokeTestProducts(BaseTestClass):
    def setUp(self):
        super(SmokeTestProducts, self).setUp()
        self.products_page = ProductsPage(self.driver)

    def tearDown(self):
        super(SmokeTestProducts, self).tearDown()

    def test_C60_CheckProductsPageDisplayedCorrectly(self):
        # Setup
        title = 'Products'
        subtitle = 'Manage products and their preferences.'

        # Assert
        self.assertEqual(title, self.products_page.title)
        self.assertEqual(subtitle, self.products_page.subtitle)

    def test_C61_CheckProductAdded(self):
        # Setup
        product_name = StringMethods.get_unique_name('product_name_')
        display = StringMethods.get_unique_name('pn_')
        sage = StringMethods.get_unique_digit()
        default_cut = DefaultCut.whole

        self.addCleanup(self.products_page.remove_entry, product_name)

        # Action
        self.products_page.add_entry(product_name, display, sage, default_cut)

        # Assert
        product_row = self.products_page.table.get_row_for_field_value(HeadersProducts.Name, product_name)
        self.assertIsNotNone(product_row)
        self.assertEqual(product_name, product_row[HeadersProducts.Name])
        self.assertEqual(display, product_row[HeadersProducts.DisplayName])
        self.assertEqual(sage, product_row[HeadersProducts.SageProductCode])
        self.assertEqual(default_cut, product_row[HeadersProducts.DefaultCut])

    def test_C62_CheckProductEdited(self):
        # Setup
        product_name = StringMethods.get_unique_name('product_name_')
        display = StringMethods.get_unique_name('pn_')
        sage = StringMethods.get_unique_digit()
        default_cut = DefaultCut.whole

        # Setup - edit
        product_name_edited = StringMethods.get_unique_name('product_name_')
        display_edited = StringMethods.get_unique_name('pn_')
        sage_edited = StringMethods.get_unique_digit()
        default_cut_edited = DefaultCut.butterfly

        self.addCleanup(self.products_page.remove_entry, product_name_edited)

        # Action
        self.products_page.add_entry(product_name, display, sage, default_cut)
        product_row = self.products_page.table.get_row_for_field_value(HeadersProducts.Name, product_name)
        self.products_page.edit_entry(product_row, product_name_edited, display_edited, sage_edited, default_cut_edited)

        # Assert
        self.products_page.wait_for_page()
        product_row = self.products_page.table.get_row_for_field_value(HeadersProducts.Name, product_name_edited)
        self.assertIsNotNone(product_row)
        self.assertEqual(product_name_edited, product_row[HeadersProducts.Name])

    def test_C63_CheckProductRemoved(self):
        # Setup
        no_products_message = 'There is no data to display'
        product_name = StringMethods.get_unique_name('product_name_')
        display = StringMethods.get_unique_name('pn_')
        sage = StringMethods.get_unique_digit()
        default_cut = DefaultCut.whole

        # Action
        self.products_page.add_entry(product_name, display, sage, default_cut)
        products_row = self.products_page.table.get_row_for_field_value(HeadersProducts.Name, product_name)
        self.products_page.delete_row(products_row)

        # Assert
        self.assertEqual(no_products_message, self.products_page.empty_text)

    def test_C64_CheckNewProductRightDetails(self):
        # Setup
        product_name = StringMethods.get_unique_name('product_name_')
        display = StringMethods.get_unique_name('pn_')
        sage = StringMethods.get_unique_digit()
        default_cut = DefaultCut.whole

        # Action
        self.products_page.add_entry(product_name, display, sage, default_cut)
        products_row = self.products_page.table.get_row_for_field_value(HeadersProducts.Name, product_name)
        products_row.details_row_item.click()
        check_dialog = ProductsCheckDialog(self.driver)

        # Assert
        self.assertEqual(product_name, check_dialog.product_name)

        check_dialog.remove_entry(product_name)

    def test_C65_CheckProductDetailsThenEdit(self):
        # Setup
        product_name = StringMethods.get_unique_name('product_name_')
        display = StringMethods.get_unique_name('pn_')
        sage = StringMethods.get_unique_digit()
        default_cut = DefaultCut.whole

        # Setup - edit
        product_name_edited = StringMethods.get_unique_name('product_name_')
        display_edited = StringMethods.get_unique_name('pn_')
        sage_edited = StringMethods.get_unique_digit()
        default_cut_edited = DefaultCut.whole

        self.addCleanup(self.products_page.remove_entry, product_name_edited)

        # Action
        self.products_page.add_entry(product_name, display, sage, default_cut)

        products_row = self.products_page.table.get_row_for_field_value(HeadersProducts.Name, product_name)
        products_row.details_row_item.click()
        check_dialog = ProductsCheckDialog(self.driver)
        check_dialog.edit_entry(product_name_edited, display_edited, sage_edited, default_cut_edited)

        # Assert
        products_row = self.products_page.table.get_row_for_field_value(HeadersProducts.Name, product_name_edited)
        self.assertIsNotNone(products_row)
        self.assertEqual(product_name_edited, products_row[HeadersProducts.Name])

    def test_C66_CheckProductDetailsThenDelete(self):
        # Setup
        no_products_message = 'There is no data to display'
        product_name = StringMethods.get_unique_name('product_name_')
        display = StringMethods.get_unique_name('pn_')
        sage = StringMethods.get_unique_digit()
        default_cut = DefaultCut.whole

        # Action
        self.products_page.add_entry(product_name, display, sage, default_cut)

        products_row = self.products_page.table.get_row_for_field_value(HeadersProducts.Name, product_name)
        products_row.details_row_item.click()
        check_dialog = ProductsCheckDialog(self.driver)
        check_dialog.remove_entry(product_name)

        # Assert
        self.assertEqual(no_products_message, self.products_page.empty_text)



    def test_C130_CheckNoDuplicateEntriesAllowed(self):
        # fails because duplication is allowed
        # Setup
        product_name = StringMethods.get_unique_name('product_name_')
        display = StringMethods.get_unique_name('pn_')
        sage = StringMethods.get_unique_digit()
        default_cut = DefaultCut.whole

        expected_error = 'Duplicate entries are not allowed.'

        # Action
        self.products_page.add_entry(product_name, display, sage, default_cut)
        confirmation_dialog = ConfirmationMessageDialog(self.webdriver)
        confirmation_dialog.ok_button.click()
        PrintMessage('Product created.')
        products_page = ProductsPage(self.driver)
        products_page.add_button.click()
        add_dialog = ProductsAddDialog(self.driver)
        add_dialog.name.send_keys(product_name)
        add_dialog.display.send_keys(display)
        add_dialog.sage.send_keys(sage)
        add_dialog.default_cut.select_input(default_cut)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()
        product_name.remove_entry(product_name)




