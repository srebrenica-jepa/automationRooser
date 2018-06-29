

class BasePage(object):

    def __init__(self, webdriver):
        self.webdriver = webdriver

    def navigate(self):
        return

    def wait(self):
        return

    def load(self):
        self.navigate()
        self.wait()

