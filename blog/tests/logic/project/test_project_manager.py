from django.test import TestCase
from blog.logic.project.project_manager import ProjectManager
from blog import views
import os


class ProjectManagerTest(TestCase):
	def setUp(self):
		self.base_dir = os.path.dirname(os.path.dirname(views.__file__))
		self.project_manager = ProjectManager()

	def tearDown(self):
		self.project_manager = None

	def test_search_dir_for_projects(self):
		result = self.project_manager.search_dir_for_projects(path=self.base_dir)
		self.assertEquals(1, len(result))

	def test_define_project_type(self):
		result = self.project_manager.define_project_type(path=self.base_dir)
		self.assertEquals(result, 'django')