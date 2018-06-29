#!/usr/bin/env python


class TableRowField(object):
    def __init__(self, row_field_element):
        self._row_element = row_field_element

    @property
    def text(self):
        return self._row_element.text
