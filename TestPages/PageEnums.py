#!/usr/bin/env python
####################################################################################################################
# Temporary storage


class CheckOneBox(object):
    yes = 1
    no = 0


class Currency(object):
    Pound = '&#163'
    Euro = '&#8364'
    Dollar = '&#36'


class Weight(object):
    Kg = 0
    St = 1


class DefaultCut(object):
    whole = 'whole'
    headless = 'headless'
    butterfly = 'butterfly'


class UserRole(object):
    Buyer = 'Buyer'
    Manager = 'Manager'
    Salesman = 'Salesman'
    Paletter = 'Paletter'
    FactoryStaff = 'Factory Staff'
    Transporter = 'Transporter'
    Dispatch1 = 'Dispatch 1'
    Dispatch2 = 'Dispatch 2'

####################################################################################################################


class TableHeaders(object):
    """
    Basic entries
    """
    Name = 'Name'


class State(object):
    # to set
    Enable = 'Enable'
    Disable = 'Disable'

    # already set
    Enabled = 'Enabled'
    Disabled = 'Disabled'


class HeadersPuchases(object):
    PassedAt = 'Passed at'
    BoxesKG = 'Boxes x KG'
    BoxCost = 'Box cost'
    AvgCost = 'Avg cost/kg'
    TotalKg = 'Total kg'
    Species = 'Species'
    Boat = 'Boat'


class HeadersSales(object):
    Dispatch = 'Dispatch'
    Customer = 'Customer'
    Transport = 'Transport'
    Items = 'Items'
    Status = 'Status'
    Invoiced = 'Invoiced'


class HeadersUsers(object):
    FirstName = 'First name'
    LastName = 'Last name'
    Email = 'Email'
    Role = 'Role'


class HeadersProducts(TableHeaders):
    DisplayName = 'Display name'
    SageProductCode = 'Sage Product Code'
    DefaultCut = 'Default cut'


class HeadersCustomers(TableHeaders):
    SageCode = 'Sage Code'
    Transport = 'Transport'
    Currency = 'Currency'


class HeadersBoats(TableHeaders):
    Supplier = 'Supplier'


class HeadersMarkets(TableHeaders):
    NumberOfDoors = 'Number of doors'
    DeliveryTime = 'Delivery time'


class HeadersTransports(TableHeaders):
    Delivery = 'Deliver to customers?'
    Weight = 'Min weight per order'
