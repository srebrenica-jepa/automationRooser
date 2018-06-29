#!/usr/bin/env python
from TestPages.WebdriverFunctions.WebdriverFind import WebdriverFind
from TestPages.TestPageObjects.CTAButton import CTAButton, CTAButton


class CheckBox(CTAButton):

    def click(self):
        self.element.click()
