#!/usr/bin/env python
####################################################################################################################
# Temporary storage


class SuppressAlerts(object):
    no_alerts = 0
    service_status_alerts = 1
    attack_status_alerts = 2
    service_status_alerts_and_attack_status_alerts = 3


class AlertTo(object):
    msp_admins = 1
    msp_users = 2
    tenants_admins = 3
    tenants_users = 4


class SwitchAddDialogTabs(object):
    only_general_tab = 0
    general_and_service_level_alerts_tabs = 1
    general_and_attack_status_alerts_tabs = 2
    all_tabs = 3



####################################################################################################################


class TableHeaders(object):
    """
    Basic entries
    """
    Name = 'Name'
    Description = 'Description'
    Actions = 'Actions'


class State(object):
    # to set
    Enable = 'Enable'
    Disable = 'Disable'

    # already set
    Enabled = 'Enabled'
    Disabled = 'Disabled'


class MSPRole(object):
    MSPUser = 'MSP User'
    MSPAdministrator = 'MSP Admin'


class Role(object):
    TenantAdministrator = 'Tenant Administrator'


class Timezone(object):
    gmt_plus_12 = '(GMT+12:00) Auckland, Wellington, Fiji, Kamchatka'
    gmt_plus_11 = '(GMT+11:00) Magadan, Solomon Islands, New Caledonia'
    gmt_plus_10 = '(GMT+10:00) Eastern Australia, Guam, Vladivostok'
    gmt_plus_9 = '(GMT+09:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk'
    gmt_plus_8 = '(GMT+08:00) Beijing, Perth, Singapore, Hong Kong'
    gmt_plus_7 = '(GMT+07:00) Bangkok, Hanoi, Jakarta'
    gmt_plus_6 = '(GMT+06:00) Tokyo, Seoul, Osaka, Sapporo, Yakutsk'
    gmt_plus_5 = '(GMT+05:00) Ekaterinburg, Islamabad, Karachi, Tashkent'
    gmt_plus_4 = '(GMT+04:00) Abu Dhabi, Muscat, Baku, Tbilisi'
    gmt_plus_3_30 = '(GMT+03:30) Tehran'
    gmt_plus_3 = '(GMT+03:00) Baghdad, Riyadh, Moscow, St. Petersburg'
    gmt_plus_2 = '(GMT+02:00) Kaliningrad, South Africa'
    gmt_plus_1 = '(GMT+01:00) Brussels, Copenhagen, Madrid, Paris'
    gmt_0 = '(GMT+00:00) Western Europe Time, London, Lisbon'
    gmt_minus_1 = '(GMT-01:00) Azores, Cape Verde Islands'
    gmt_minus_2 = '(GMT-02:00) Mid-Atlantic'
    gmt_minus_3 = '(GMT-03:00) Brazil, Buenos Aires, Georgetown'
    gmt_minus_3_30 = '(GMT-03:30) Newfoundland'
    gmt_minus_4 = '(GMT-04:00) Atlantic Time (Canada), Caracas, La Paz'
    gmt_minus_5 = '(GMT-05:00) Eastern Time (US & Canada), Bogota, Lima'
    gmt_minus_6 = '(GMT-06:00) Central Time (US & Canada), Mexico City'
    gmt_minus_7 = '(GMT-07:00) Mountain Time (US & Canada)'
    gmt_minus_8 = '(GMT-08:00) Pacific Time (US & Canada)'
    gmt_minus_9 = '(GMT-09:00) Alaska'
    gmt_minus_10 = '(GMT-10:00) Hawaii'
    gmt_minus_11 = '(GMT-11:00) Midway Island, Samoa'
    gmt_minus_12 = '(GMT-12:00) Eniwetok, Kwajalein'


class AttackStatus(object):
    UnderAttack = 'Under Attack'
    NotUnderAttack = 'Not Under Attack'


class Country(object):
    Germany = 'Germany'
    UK = 'United Kingdom'
    USA = 'United States'


class HeadersTenants(object):
    Name = 'Name'
    Level = 'Level'
    Status = 'Status'


class HeadersTenantsAttacks(object):
    AssetGroup = 'Asset Group'
    AssetName = 'Asset Name'
    IPAddress = 'IP Address'
    AttackStatus = 'Attack Status'
    StartTime = 'Start Time'
    Duration = 'Duration'
    Peak = 'Peak(Mbps)'


class HeadersTenantsAssets(object):
    AssetGroup = 'Asset Group'
    AssetName = 'Asset Name'
    IPAddress = 'IP Address'
    Actions = 'Actions'


class HeadersTenantsAssetGroups(object):
    Name = 'Name'
    IPAddresses = 'IP Addresses'
    Actions = 'Actions'


class HeadersSystemUsers(object):
    Email = 'Username/Email'
    FirstName = 'First Name'
    LastName = 'Last Name'
    Phone = 'Phone'
    Status = 'Status'
    Timezone = 'Timezone'
    Role = 'Role'
    Actions = 'Actions'


class HeadersTenantsAdministrators(HeadersSystemUsers):
    Authentication = 'Authentication'


class HeadersSystemLDAPServers(object):
    Name = 'Name'
    Host = 'Host'
    Port = 'Port'
    ConnectionType = 'Connection Type'
    ConnectTimeout = 'Connect Timeout'
    RequestTimeout = 'Request Timeout'
    Actions = 'Actions'


class HeadersSystemLDAPGroupRoleMapping(object):
    LDAPGroup = 'LDAP Group'
    Role = 'Role'
    Actions = 'Actions'


class ConnectionType(object):
    Ldap = 'ldap'
    Ldaps = 'ldaps'
    StartTls = 'start-tls'


class HeadersSystemAudit(object):
    DateTime = 'Date/Time'
    Username = 'Username'
    IPAddress = 'IPAddress'
    Action = 'Action'
    Description = 'Description'


class Action(object):
    Created = 'Created'
    Deleted = 'Deleted'
    LoggedIn = 'Logged In'
    LoggedOut = 'Logged Out'
    Edited = 'Edited'


class AuditDescription(object):
    ServicePolicy = 'ServicePolicy'
    Tenant = 'Tenant'


class HeadersSystemPolicy(object):
    ServiceLevel = 'Service Level'
    MaxMitigation = 'Max Mitigation (Gbps)'
    Description = 'Description'
    ServiceLevelAlerts = 'Service level alerts'
    AttackStatusAlerts = 'Attack status alerts'
    Actions = 'Actions'


class HeadersSystemReporting(object):
    Name = 'Name'
    Status = 'Status'
    SendTo = 'Send to'
    ReportType = 'Report Type'
    SendEvery = 'Send every'
    Time = 'Time'
    Actions = 'Actions'


class SendToServiceOverviewReport(object):
    MSPAdmin = 'MSP Administrator'
    MSPUser = 'MSP User'
    MSPAdminAndUser = 'MSP Administrator, MSP User'


class SendToPerTenantReport(SendToServiceOverviewReport):
    TenantAdmin = 'Tenant Administrator'
    TenantUser = 'Tenant User'
    MSPAdminAndTenantAdmin = 'MSP Administrator, Tenant Administrator'
    MSPAdminAndTenantUser = 'MSP Administrator, Tenant User'
    MSPUserAndTenantAdmin = 'MSP User, Tenant Administrator'
    MSPUserAndTenantUser = 'MSP User, Tenant User'
    TenantAdminAndUser = 'Tenant Administrator, Tenant User'
    MSPAdminUserAndTenantAdmin = 'MSP Administrator, MSP User, Tenant Administrator'
    MSPAdminUserAndTenantUser = 'MSP Administrator, MSP User, Tenant User'
    MSPUserTenantAdminAndUser = 'MSP User, Tenant Administrator, Tenant User'
    MSPAdminTenantAdminAndUser = 'MSP Administrator, Tenant Administrator, Tenant User'
    MSPAdminUserTenantAdminAndUser = 'MSP Administrator, MSP User, Tenant Administrator, Tenant User'


class ReportType(object):
    ServiceOverview = 'Service Overview'
    PerTenant = 'Per-Tenant'


class TimePeriod(object):
    Day = 'Day'
    Week = 'Week'
    Month = 'Month'


class InspectionMode(object):
    BlackList = 'black-list'
    WhiteList = 'white-list'
    Inspect = 'inspect'
    Monitor = 'monitor'


class HeadersLDAPServers(object):
    Name = 'Name'
    Host = 'Host'
    Port = 'Port'
    Connection_Type = 'Connection Type'
    Connect_Timeout = 'Connect Timeout'
    Request_Timeout = 'Request Timeout'
    Actions = 'Actions'


class HeadersLDAPGroupRoleMapping(object):
    LDAP_Group = 'LDAP Group'
    Role = 'Role'

