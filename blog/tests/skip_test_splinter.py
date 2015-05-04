from splinter import Browser
from django.test import LiveServerTestCase

class TestClass(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        cls.browser = Browser('zope.testbrowser')
        super(TestClass, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(TestClass, cls).tearDownClass()

    def test_google(self):
        url = "http://localhost:8081"
        self.browser.visit(url)
        self.assertTrue('<form action="/username/" method="post">' in self.browser.html)
        #print(self.browser.html)
        #self.browser.fill('username', 'testuser')
        #button = self.browser.find_by_value('OK')
        #button.click()
        #result = self.browser.is_text_present('Directory to workspace')
        #self.assertTrue(result)