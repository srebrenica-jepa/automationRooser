#!/usr/bin/env python


def list_enum(enum):
    assert type(enum) == type
    return [getattr(enum, i) for i in dir(enum) if not i.startswith('_')]


class RunTypes(object):
    AllTests = 'AllTests'
    Regression = 'Regression'
    Smoke = 'Smoke'


# TestResult is used by test rail and reporting tool
class TestResult(object):
    Passed = 1
    Blocked = 2
    Untested = 3
    Retest = 4
    Failed = 5
    Pass_wCon = 6


class UsersChoice(object):
    yes = 'yes'
    no = 'no'


class UserGroup(object):
    admin = 'cns-admin'
    defense = 'cns-defense'
    monitor = 'cns-monitor'
    support = 'cns-support'
    none = 'none'


class State(object):
    enabled = 'enabled'
    disabled = 'disabled'


class ActionResult(object):
    success = 'Success'
    failure = 'Failure'


class IPGroups(object):
    DestinationGroup = 'dgn'
    DestinationName = 'din'
    SourceGroup = 'sgn'
    SourceName = 'sin'


class DeploymentType(object):
    kvm = 'kvm'
    vmware = 'vmware'
    ntd1100 = 'ntd1100'
    gx = 'gx'


class DeviceType(object):
    ntd = 'ntd'
    sms = 'cms'
    swa = 'swa'


class KVMDeviceState(object):
    offline = 'offline'
    online = 'online'
    not_found = 'not_found'


class ControlKeys(object):
    ctr_c = '\003'
    ctr_d = '\004'


class DeviceStatus(object):
    class DeploymentState(object):
        not_licensed = 'not-licensed'
        sync_required = 'sync-required'
        force_sync_required = 'force-sync-required'
        in_sync = 'in-sync'

    class ConnectionState(object):
        connected = 'connected'

    class DeploymentAction(object):
        none = 'none'


class DefenseMode(object):
    mitigate = 'mitigate'
    monitor = 'monitor'
    #  monitor_tap = 'monitor-tap' removed
    pass_through = 'pass-through'