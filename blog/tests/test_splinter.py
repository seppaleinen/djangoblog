from splinter import Browser
from django.test import TestCase

class TestClass(TestCase):
    @classmethod
    def setUpClass(cls):
        #try:
        #    cls.selenium = webdriver.Firefox()
        #    cls.selenium.maximize_window()
        #    super(TestClass, cls).setUpClass()
        #except Exception:
        #    raise SkipTest("Firefox not installed on system")
        cls.browser = Browser('zope.testbrowser', ignore_robots=True)
        super(TestClass, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(TestClass, cls).tearDownClass()

    def test_google(self):
        # Visit URL
        url = "http://splinter.readthedocs.org/en/latest/index.html"
        self.browser.visit(url)
        #self.browser.fill('q', 'splinter - python acceptance testing for web applications')
        # Find and click the 'search' button
        #button = self.browser.find_by_name('btnG')
        # Interact with elements
        #button.click()
        if self.browser.is_text_present('Splinter is an open source'):
            print "Yes, the official website was found!"
        else:
            print "No, it wasn't found... We need to improve our SEO techniques"