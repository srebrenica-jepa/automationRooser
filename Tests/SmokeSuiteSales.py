#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.SalesAllPage import SalesAllPage
from TestPages.SalesOverviewPage import SalesOverviewPage
from TestPages.TestDialogs.SalesAllCheckDialog import SalesAllCheckDialog
from TestPages.TestDialogs.SalesAddDialog import SalesAddDialog
from TestPages.TestDialogs.SalesAllAddDialog import SalesAllAddDialog
from TestPages.TestDialogs.MessageDialog import MessageDialog
from TestPages.CustomersPage import CustomersPage
from TestPages.TransportsPage import TransportsPage
from TestPages.ProductsPage import ProductsPage
from TestHelpers import StringMethods
from TestPages.PageEnums import CheckOneBox, DefaultCut, HeadersSales


class SmokeTestSales(BaseTestClass):
    def setUp(self):
        super(SmokeTestSales, self).setUp()
        self.overview_page = SalesOverviewPage(self.driver)
        self.all_page = SalesAllPage(self.driver)

        self.customer_name = StringMethods.get_unique_name('customer_name_')
        self.sage_code = StringMethods.get_unique_name('sage_')
        self.transport_name = StringMethods.get_unique_name('transport_name_')
        self.product_name = StringMethods.get_unique_name('product_name_')
        self.display = StringMethods.get_unique_name('pn_')
        self.sage = StringMethods.get_unique_digit()
        self.default_cut = DefaultCut.whole

    def tearDown(self):
        super(SmokeTestSales, self).tearDown()

    def add_product(self, name, display, sage, default_cut=DefaultCut.whole):
        product_page = ProductsPage(self.driver)
        product_page.add_entry(name, display, sage, default_cut)

    def remove_product(self, product_name):
        product_page = ProductsPage(self.driver)
        product_page.remove_entry(product_name)

    def add_customer(self, customer_name, sage_code):
        customer_page = CustomersPage(self.driver)
        customer_page.add_entry(customer_name, sage_code)

    def remove_customer(self, customer_name):
        customer_page = CustomersPage(self.driver)
        customer_page.remove_entry(customer_name)

    def add_transport(self, transport_name, weight=None, shipping=CheckOneBox.no):
        transport_page = TransportsPage(self.driver)
        transport_page.add_entry(transport_name, weight, shipping)

    def remove_transport(self, transport_name):
        transport_page = TransportsPage(self.driver)
        transport_page.remove_entry(transport_name)

    def test_C126_CheckSalesOverviewPageDisplayedCorrectly(self):
        # Setup
        title_average = 'Average selling price per species/cut (Work in progress)'
        title_hygiene = 'Sales Hygiene Labels'
        title_fish = 'Fish Required report'
        title_invoice = 'Sales Invoice Prep'
        title_summary = 'Sales Week Summary'

        # Assert
        self.assertEqual(title_average, self.overview_page.title_average)
        self.assertEqual(title_hygiene, self.overview_page.title_hygiene)
        self.assertEqual(title_fish, self.overview_page.title_fish)
        self.assertEqual(title_invoice, self.overview_page.title_invoice)
        self.assertEqual(title_summary, self.overview_page.title_summary)

    def test_C129_CheckSalesAllPageDisplayedCorrectly(self):
        # Setup
        title = 'Sales'
        subtitle = 'Manage sales orders, add new ones or cancel. '

        self.all_page.wait()

        # Assert
        self.assertEqual(title, self.all_page.title)
        self.assertEqual(subtitle, self.all_page.subtitle)

    def test_C153_CheckSaleAddedTransportThatDeliversToCustomersWithNoMinWeight(self):
        # Setup
        cut = DefaultCut.whole
        quantity = StringMethods.get_unique_digit()
        weight = StringMethods.get_unique_digit()
        price = StringMethods.get_unique_digit()

        # Action
        self.add_customer(self.customer_name, self.sage_code)
        self.add_transport(self.transport_name,shipping=CheckOneBox.yes)
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        sale_page = SalesAllPage(self.driver)
        sale_page.add_entry(self.customer_name, self.transport_name, self.product_name, cut, quantity, weight, price)

        # Assert
        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        self.assertIsNotNone(sales_row)
        self.assertEqual(self.customer_name, sales_row[HeadersSales.Customer])

        sale_page.remove_entry(self.customer_name)

        self.remove_customer(self.customer_name)
        self.remove_transport(self.transport_name)

    def test_C155_CheckSaleEditedTransportThatDeliversToCustomersWithNoMinWeight(self):
        # Setup
        cut = DefaultCut.whole
        quantity = StringMethods.get_unique_digit()
        weight = StringMethods.get_unique_digit()
        price = StringMethods.get_unique_digit()

        # Setup - edit
        cut_edited = DefaultCut.headless
        quantity_edited = StringMethods.get_unique_digit()
        weight_edited = StringMethods.get_unique_digit()
        price_edited = StringMethods.get_unique_digit()

        # Action
        self.add_customer(self.customer_name, self.sage_code)
        self.add_transport(self.transport_name,shipping=CheckOneBox.yes)
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        sale_page = SalesAllPage(self.driver)
        sale_page.add_entry(self.customer_name, self.transport_name, self.product_name, cut, quantity, weight, price)

        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        sale_page.edit_entry(self.customer_name, self.transport_name, self.product_name, cut_edited, quantity_edited, weight_edited, price_edited)

        # Assert
        sale_page.wait()
        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        self.assertIsNotNone(sales_row)
        self.assertEqual(self.customer_name, sales_row[HeadersSales.Customer])
        self.assertEqual(quantity_edited, sales_row[HeadersSales.Items])

        sale_page.remove_entry(self.customer_name)

        self.remove_customer(self.customer_name)
        self.remove_transport(self.transport_name)


    def test_C156_CheckSaleRemovedTransportThatDeliversToCustomersWithNoMinWeight(self):
        # Setup
        cut = DefaultCut.whole
        quantity = StringMethods.get_unique_digit()
        weight = StringMethods.get_unique_digit()
        price = StringMethods.get_unique_digit()

        # Action
        self.add_customer(self.customer_name, self.sage_code)
        self.add_transport(self.transport_name,shipping=CheckOneBox.yes)
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        sale_page = SalesAllPage(self.driver)
        sale_page.add_entry(self.customer_name, self.transport_name, self.product_name, cut, quantity, weight, price)

        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        sales_row.delete_row(sales_row)

        # Assert
        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        self.assertIsNone(sales_row)

        self.remove_customer(self.customer_name)
        self.remove_transport(self.transport_name)

    def test_C157_CheckNewSaleRightDetailsTransportThatDeliversToCustomersWithNoMinWeight(self):
        # Setup
        cut = DefaultCut.whole
        quantity = StringMethods.get_unique_digit()
        weight = StringMethods.get_unique_digit()
        price = StringMethods.get_unique_digit()

        # Action
        self.add_customer(self.customer_name, self.sage_code)
        self.add_transport(self.transport_name,shipping=CheckOneBox.yes)
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        sale_page = SalesAllPage(self.driver)
        sale_page.add_entry(self.customer_name, self.transport_name, self.product_name, cut, quantity, weight, price)

        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        sales_row.details_row_item.click()
        check_dialog = SalesAllCheckDialog(self.driver)

        # Assert
        self.assertEqual(self.customer_name, check_dialog.customer_name)

        check_dialog.remove_entry(self.customer_name)

        self.remove_customer(self.customer_name)
        self.remove_transport(self.transport_name)

    def test_C158_CheckSaleDetailsThenEditTransportThatDeliversToCustomersWithNoMinWeight(self):
        # Setup
        cut = DefaultCut.whole
        quantity = StringMethods.get_unique_digit()
        weight = StringMethods.get_unique_digit()
        price = StringMethods.get_unique_digit()

        # Setup - edit
        cut_edited = DefaultCut.headless
        quantity_edited = StringMethods.get_unique_digit()
        weight_edited = StringMethods.get_unique_digit()
        price_edited = StringMethods.get_unique_digit()

        # Action
        self.add_customer(self.customer_name, self.sage_code)
        self.add_transport(self.transport_name,shipping=CheckOneBox.yes)
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        sale_page = SalesAllPage(self.driver)
        sale_page.add_entry(self.customer_name, self.transport_name, self.product_name, cut, quantity, weight, price)

        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        sales_row.details_row_item.click()
        check_dialog = SalesAllCheckDialog(self.driver)
        check_dialog.edit_entry(self.customer_name, self.transport_name, self.product_name, cut_edited, quantity_edited, weight_edited, price_edited)

        # Assert
        sale_page = SalesAllPage(self.driver)
        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        self.assertIsNotNone(sales_row)
        self.assertEqual(quantity_edited, sales_row[HeadersSales.Items])

        sale_page.remove_entry(self.customer_name)

        self.remove_customer(self.customer_name)
        self.remove_transport(self.transport_name)

    def test_C159_CheckSaleDetailsThenDeleteTransportThatDeliversToCustomersWithNoMinWeight(self):
        # Setup
        cut = DefaultCut.whole
        quantity = StringMethods.get_unique_digit()
        weight = StringMethods.get_unique_digit()
        price = StringMethods.get_unique_digit()
        no_sales_message = 'There is no data to display'

        # Action
        self.add_customer(self.customer_name, self.sage_code)
        self.add_transport(self.transport_name,shipping=CheckOneBox.yes)
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        sale_page = SalesAllPage(self.driver)
        sale_page.add_entry(self.customer_name, self.transport_name, self.product_name, cut, quantity, weight, price)

        sales_row = sale_page.table.get_row_for_field_value(HeadersSales.Customer, self.customer_name)
        sales_row.details_row_item.click()
        check_dialog = SalesAllCheckDialog(self.driver)
        check_dialog.remove_entry(self.customer_name)

        # Assert
        self.assertEqual(no_sales_message, sale_page.empty_text)

        self.remove_customer(self.customer_name)
        self.remove_transport(self.transport_name)

    def test_C160_CheckMinimumWeightPerOrderValidation(self):
        # Setup
        cut = DefaultCut.whole
        quantity = StringMethods.get_unique_digit()
        weight = StringMethods.get_unique_digit()
        price = StringMethods.get_unique_digit()

        min_weight = StringMethods.get_unique_digit()

        error_message = 'Min. weight required'

        # Action
        self.add_customer(self.customer_name, self.sage_code)
        self.add_transport(self.transport_name,weight=min_weight, shipping=CheckOneBox.yes)
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)

        sale_page = SalesAllPage(self.driver)
        sale_page.add_button.click()
        add_dialog = SalesAllAddDialog(self.driver)
        add_dialog.customer.select_input_enter(self.customer_name)
        add_dialog.new_sale.click()
        add_dialog.wait()
        add_dialog.transport.select_input_enter(self.transport_name)
        add_dialog.product.select_input_enter(self.product_name)
        add_dialog.new_sale.click()
        add_dialog.add_button.click()
        add_dialog_s= SalesAddDialog(self.driver)
        add_dialog_s.cut.select_input_enter(cut)
        add_dialog_s.quantity.send_keys(quantity)
        add_dialog_s.weight.send_keys(str(min(int(weight),int(min_weight))-1))
        add_dialog_s.price.send_keys(price)
        add_dialog_s.add_button.click()

        message_dialog = MessageDialog(self.driver)

        # Assert
        self.assertEqual(error_message, message_dialog.title)

        self.remove_customer(self.customer_name)
        self.remove_transport(self.transport_name)

    def test_C161_CheckSaleValidationTransportThatDoeNotDeliverToCustomersWithNoMinWeight(self):
        # Setup
        cut = DefaultCut.whole
        quantity = StringMethods.get_unique_digit()
        weight = StringMethods.get_unique_digit()
        price = StringMethods.get_unique_digit()

        error_message = 'A transport that delivers to customer is required'

        # Action
        self.add_customer(self.customer_name, self.sage_code)
        self.add_transport(self.transport_name,shipping=CheckOneBox.no)
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)

        sale_page = SalesAllPage(self.driver)
        sale_page.add_button.click()
        add_dialog = SalesAllAddDialog(self.driver)
        add_dialog.customer.select_input_enter(self.customer_name)
        add_dialog.new_sale.click()
        add_dialog.wait()
        add_dialog.product.select_input_enter(self.product_name)
        add_dialog.new_sale.click()
        add_dialog.add_button.click()
        add_dialog_s= SalesAddDialog(self.driver)
        add_dialog_s.cut.select_input_enter(cut)
        add_dialog_s.quantity.send_keys(quantity)
        add_dialog_s.weight.send_keys(weight)
        add_dialog_s.price.send_keys(price)
        add_dialog_s.add_button.click()


        # Assert
        add_dialog_s.is_text_present(error_message)

        self.remove_customer(self.customer_name)
        self.remove_transport(self.transport_name)