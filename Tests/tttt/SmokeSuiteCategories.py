#!/usr/bin/env python
from Tests.BaseTestClass import BaseTestClass
from TestPages.CategoriesPage import CategoriesPage
from TestPages.SpeciesPage import SpeciesPage
from TestPages.ProductsPage import ProductsPage
from TestPages.TestDialogs.CategoriesAddDialog import CategoriesAddDialog
from TestPages.TestDialogs.CategoriesCheckDialog import CategoriesCheckDialog
from TestHelpers import StringMethods
from TestPages.PageEnums import TableHeaders, DefaultCut


class SmokeTestCategories(BaseTestClass):
    def setUp(self):
        super(SmokeTestCategories, self).setUp()
        self.categories_page = CategoriesPage(self.driver)
        self.species_name = StringMethods.get_unique_name('species_name_')
        self.product_name = StringMethods.get_unique_name('product_name_')
        self.display = StringMethods.get_unique_name('pn_')
        self.sage = StringMethods.get_unique_digit()
        self.default_cut = DefaultCut.whole

    def tearDown(self):
        super(SmokeTestCategories, self).tearDown()

    def add_species(self, name):
        species_page = SpeciesPage(self.driver)
        species_page.add_entry(name)

    def remove_species(self, name):
        species_page = SpeciesPage(self.driver)
        species_page.remove_entry(name)

    def add_product(self, name, display, sage, default_cut):
        product_page = ProductsPage(self.driver)
        product_page.add_entry(name, display, sage, default_cut)

    def remove_product(self, name):
        product_page = ProductsPage(self.driver)
        product_page.remove_entry(name)


    def test_C72_CheckCategoriesPageDisplayedCorrectly(self):
        # Setup
        title = 'Categories'
        subtitle = 'Manage categories and their products/species.'

        # Assert
        self.assertEqual(title, self.categories_page.title)
        self.assertEqual(subtitle, self.categories_page.subtitle)

    def test_C73_CheckCategoryAdded(self):
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')

        # Action
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        self.add_species(self.species_name)
        categories_page = CategoriesPage(self.driver)
        categories_page.add_entry(category_name, self.species_name, self.product_name)

        # Assert
        category_row = categories_page.table.get_row_for_field_value(TableHeaders.Name, category_name)
        self.assertIsNotNone(category_row)
        self.assertEqual(category_name, category_row[TableHeaders.Name])

        categories_page.remove_entry(category_name)

        self.remove_product(self.product_name)
        self.remove_species(self.species_name)

    def test_C74_CheckCategoryEdited(self):
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')

        # Setup - edit
        category_name_edited = StringMethods.get_unique_name('category_name_edited_')

        # Action
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        self.add_species(self.species_name)
        categories_page = CategoriesPage(self.driver)
        categories_page.add_entry(category_name, self.species_name, self.product_name)
        category_row = categories_page.table.get_row_for_field_value(TableHeaders.Name, category_name)
        categories_page.edit_entry(category_row, category_name_edited, self.species_name, self.product_name)

        # Assert
        category_row = categories_page.table.get_row_for_field_value(TableHeaders.Name, category_name_edited)
        self.assertIsNotNone(category_row)
        self.assertEqual(category_name_edited, category_row[TableHeaders.Name])

        categories_page.remove_entry(category_name_edited)

        self.remove_product(self.product_name)
        self.remove_species(self.species_name)

    def test_C75_CheckCategoryRemoved(self):
        # Setup
        no_categories_message = 'There is no data to display'
        category_name = StringMethods.get_unique_name('category_name_')

        # Action
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        self.add_species(self.species_name)
        categories_page = CategoriesPage(self.driver)
        categories_page.add_entry(category_name, self.species_name, self.product_name)
        category_row = categories_page.table.get_row_for_field_value(TableHeaders.Name, category_name)
        categories_page.delete_row(category_row)

        # Assert
        self.assertEqual(no_categories_message, categories_page.empty_text)

        self.remove_product(self.product_name)
        self.remove_species(self.species_name)

    def test_C76_CheckNewCategoryRightDetails(self):
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')

        # Action
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        self.add_species(self.species_name)
        categories_page = CategoriesPage(self.driver)
        categories_page.add_entry(category_name, self.species_name, self.product_name)
        category_row = categories_page.table.get_row_for_field_value(TableHeaders.Name, category_name)
        category_row.details_row_item.click()
        check_dialog = CategoriesCheckDialog(self.driver)

        # Assert
        self.assertEqual(category_name, check_dialog.category_name)

        check_dialog.remove_entry(category_name)

        self.remove_product(self.product_name)
        self.remove_species(self.species_name)

    def test_C77_CheckCategoryDetailsThenEdit(self):
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')

        # Setup - edit
        category_name_edited = StringMethods.get_unique_name('category_name_edited_')

        # Action
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        self.add_species(self.species_name)
        categories_page = CategoriesPage(self.driver)
        categories_page.add_entry(category_name, self.species_name, self.product_name)
        category_row = categories_page.table.get_row_for_field_value(TableHeaders.Name, category_name)
        category_row.details_row_item.click()
        check_dialog = CategoriesCheckDialog(self.driver)
        check_dialog.edit_entry(category_name_edited, self.species_name, self.product_name)

        # Assert
        categories_page = CategoriesPage(self.driver)
        category_row = categories_page.table.get_row_for_field_value(TableHeaders.Name, category_name_edited)
        self.assertIsNotNone(category_row)
        self.assertEqual(category_name_edited, category_row[TableHeaders.Name])

        categories_page.remove_entry(category_name_edited)

        self.remove_product(self.product_name)
        self.remove_species(self.species_name)

    def test_C78_CheckCategoryDetailsThenDelete(self):
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        no_categories_message = 'There is no data to display'

        # Action
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        self.add_species(self.species_name)
        categories_page = CategoriesPage(self.driver)
        categories_page.add_entry(category_name, self.species_name, self.product_name)
        category_row = categories_page.table.get_row_for_field_value(TableHeaders.Name, category_name)
        category_row.details_row_item.click()
        check_dialog = CategoriesCheckDialog(self.driver)
        check_dialog.remove_entry(category_name)

        # Assert
        self.assertEqual(no_categories_message, categories_page.empty_text)

    def test_C79_CheckNoCategoryNameValidation(self):
        # Setup
        expected_error = 'Category name is required'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C80_CheckIncorrectCategoryNameValidation(self):
        # Setup
        category_name = '@'
        expected_error = 'PLEASE ENTER A NAME OF AT LEAST 3 CHARACTERS'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C81_CheckNoSpeciesValidation(self):
        # fails because the field is not mandatory
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        expected_error = 'PLEASE SELECT AT LEAST ONE'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.species.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C82_CheckNoSalesValidation(self):
        # fails because the field is not mandatory
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        expected_error = 'PLEASE SELECT AT LEAST ONE'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.sales.click()
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C83_CheckIncorrectWholeYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        whole = '-1'
        expected_error = 'Whole yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.whole.send_keys(whole)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C84_CheckIncorrectHeadlessYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        headless = '-1'
        expected_error = 'Headless yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.headless.send_keys(headless)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C85_CheckIncorrectOnOnYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        on_on = '-1'
        expected_error = 'Filet skin on fap on yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.on_on.send_keys(on_on)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C86_CheckIncorrectOnOffYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        on_off = '-1'
        expected_error = 'Filet skin on fap off yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.on_off.send_keys(on_off)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C87_CheckIncorrectOffOnYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        off_on = '-1'
        expected_error = 'Filet skin off fap on yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.off_on.send_keys(off_on)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C88_CheckIncorrectOffOffYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        off_off = '-1'
        expected_error = 'Filet skin off fap off yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.off_off.send_keys(off_off)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C89_CheckIncorrectJCutOnYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        j_cut_on = '-1'
        expected_error = 'Filet j-cut skin on yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.j_cut_on.send_keys(j_cut_on)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C90_CheckIncorrectJCutOffYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        j_cut_off = '-1'
        expected_error = 'Filet j-cut skin off yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.j_cut_off.send_keys(j_cut_off)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C91_CheckIncorrectButterflyYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        butterfly = '-1'
        expected_error = 'Butterfly yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.butterfly.send_keys(butterfly)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C92_CheckIncorrectOffVCutYieldValidation(self):
        # fails due to the fact that the wrong format is accepted
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')
        off_v = '-1'
        expected_error = 'Skin off v cut yield should be greater than or equal to 0'

        # Action
        self.categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.off_v.send_keys(off_v)
        add_dialog.save_button.click()

        # Assert
        add_dialog.is_text_present(expected_error)

        add_dialog.cancel_button.click()

    def test_C93_CheckNoDuplicationValidation(self):
        # fails dbecause duplication is allowed
        # Setup
        category_name = StringMethods.get_unique_name('category_name_')

        expected_error = 'Duplicate entries are not allowed.'

        # Action
        self.add_product(self.product_name, self.display, self.sage, self.default_cut)
        self.add_species(self.species_name)
        categories_page = CategoriesPage(self.driver)
        categories_page.add_entry(category_name, self.species_name, self.product_name)
        categories_page = CategoriesPage(self.driver)
        categories_page.add_button.click()
        add_dialog = CategoriesAddDialog(self.driver)
        add_dialog.name.send_keys(category_name)
        add_dialog.species.select_input_enter(self.species_name)
        add_dialog.product.select_input_enter(self.product_name)
        add_dialog.save_button.click()

        # Assert

        add_dialog.cancel_button.click()
        categories_page = CategoriesPage(self.driver)
        categories_page.remove_entry(category_name)

        self.remove_product(self.product_name)
        self.remove_species(self.species_name)


