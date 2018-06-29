#!/usr/bin/env python


class Versions(list):
    def active(self):
        """
        Returns first active version as Version obj
        :return:
        """
        if True in [k['active'] for k in self.__iter__()]:
            return Version([k for k in self.__iter__() if k["active"]][0]['version'])
        else:
            return None

    def inactive(self):
        """
        Returns first inactive version as Version obj
        :return:
        """
        if False in [k['active'] for k in self.__iter__()]:
            return Version([k for k in self.__iter__() if not k["active"]][0]['version'])
        else:
            return None


class Version(object):
    def __init__(self, version_number):
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.build = None

        if type(version_number) is str or type(version_number) is unicode:
            self._init_from_string(version_number)

        elif type(version_number) is Version:
            self._init_from_obj(version_number)

        else:
            raise TypeError('unexpected initializing value {0}, type {1}'.format(version_number, type(version_number)))

    def __eq__(self, other):
        return self.major == other.major and \
               self.minor == other.minor and \
               self.patch == other.patch and \
               self.build == other.build

    def verify(self):
        assert self.major >= 0, "expected major value greater than zero"
        assert self.minor >= 0, "expected minor value greater than zero"
        assert self.patch >= 0, "expected patch value greater than zero"
        assert self.build >= 0, "expected build value greater than zero"

    def _init_from_string(self, version_number):
        version_list = version_number.split('.')
        self.major = int(version_list[0])
        self.minor = int(version_list[1])
        self.patch = int(version_list[2])

        if len(version_list) == 4:
            self.build = int(version_list[3])

    def _init_from_obj(self, version_number):
        self.major = version_number.major
        self.minor = version_number.minor
        self.patch = version_number.patch
        self.build = version_number.build

    def get_as_string(self, fill_with_zeros=4):
        layout = '{0}.{1}.{2}.{3}'
        return layout.format(self.major, self.minor, self.patch, str(self.build).zfill(fill_with_zeros))

    @property
    def release_version(self):
        layout = '{0}.{1}.{2}'
        return layout.format(self.major, self.minor, self.patch)
