#!/usr/bin/python -u
from xml.dom import minidom


def get_value_for_element(xml_string, element_name):
    xml_dom = minidom.parseString(xml_string)
    values_found = []
    for element in xml_dom.getElementsByTagName(element_name):
        values_found.append(element.firstChild.nodeValue)

    return values_found
