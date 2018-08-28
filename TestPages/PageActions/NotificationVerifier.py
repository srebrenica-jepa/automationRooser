from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from Common.Utilities.Logging import PrintMessage

from TestHelpers.ExpectedConditions import text_to_be_present_in_element


class ElementType(object):
    specific_element_type = 1
    any_element_type = 2


class NotificationVerifier(object):
    def __init__(self, webdriver, element_type=ElementType.specific_element_type):
        self.webdriver = webdriver
        self.element_type = element_type

    def is_text_present(self, notification_text, element_type=ElementType.specific_element_type, element_index=0, by_type=By.CSS_SELECTOR, value=".error"):
        if element_type == ElementType.specific_element_type:

            notification_field = text_to_be_present_in_element((by_type, value), notification_text, element_index)
            try:
                PrintMessage('Making an attempt to check for notification: {0}'.format(notification_text))
                WebDriverWait(self.webdriver, 20).until(notification_field)
            except TimeoutException:
                return False

        elif element_type == ElementType.any_element_type:

            text_to_be_present_in_element((by_type, value), notification_text)
            PrintMessage('Making an attempt to check for notification: {0}'.format(notification_text))

        return True
