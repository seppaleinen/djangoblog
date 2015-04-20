from selenium import webdriver

from selenium.webdriver.common.keys import Keys
from django.test import LiveServerTestCase
from django.utils.unittest import SkipTest

class SeleniumTestCase(LiveServerTestCase):
	@classmethod
	def setUpClass(cls):
		try:
			cls.selenium = webdriver.Firefox()
			cls.selenium.maximize_window()
			super(SeleniumTestCase, cls).setUpClass()
		except Exception:
			raise SkipTest("Firefox not installed on system")

	@classmethod
	def tearDownClass(cls):
		cls.selenium.quit()
		super(SeleniumTestCase, cls).tearDownClass()

	def testFirstPage(self):
		self.selenium.get("%s" % self.live_server_url)
		search_box = self.selenium.find_element_by_id("your_name")
		search_box.send_keys("testing")
		search_box.send_keys(Keys.RETURN)
		assert "testing" in self.selenium.find_element_by_class_name("user").text

	def testFirstPage2(self):
		self.selenium.get("%s" % self.live_server_url)
		search_box = self.selenium.find_element_by_id("your_name")
		search_box.send_keys("testing")
		search_box.send_keys(Keys.RETURN)
		assert "testing" in self.selenium.find_element_by_class_name("user").text