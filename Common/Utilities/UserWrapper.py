#!/usr/bin/env python


class UserWrapper(object):
    def __init__(self, name, password, group=None):
        self.name = name
        self.group = group
        self.password = password

    @staticmethod
    def copy(user):
        assert type(user) == UserWrapper
        return UserWrapper(user.name,
                           user.password,
                           user.group)
