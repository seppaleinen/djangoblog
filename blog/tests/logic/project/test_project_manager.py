from django.test import TestCase
from blog.logic.project.project_manager import ProjectManager
from blog import views
import os
from blog.tests.resources import maven


class ProjectManagerTest(TestCase):
	@classmethod
	def setUpClass(cls):
		cls.base_dir = os.path.dirname(os.path.dirname(views.__file__))
		super(ProjectManagerTest, cls).setUpClass()

	def setUp(self):
		self.project_manager = ProjectManager()

	def tearDown(self):
		self.project_manager = None

	def test_search_dir_for_projects(self):
		result = self.project_manager.search_dir_for_projects(path=self.base_dir)
		self.assertEquals(1, len(result))

	def test_define_project_type_django(self):
		result = self.project_manager.define_project_type(path=self.base_dir)
		self.assertEquals(result, 'django')

	def test_define_project_type_maven(self):
		maven_path = os.path.join(os.path.dirname(os.path.dirname(maven.__file__)), 'maven')
		result = self.project_manager.define_project_type(path=maven_path)
		self.assertEquals(result, 'maven')

	def test_define_project_type_gradle(self):
		gradle_path = os.path.join(os.path.dirname(os.path.dirname(maven.__file__)), 'gradle')
		result = self.project_manager.define_project_type(path=gradle_path)
		self.assertEquals(result, 'gradle')

	def test_define_project_type_pysetup(self):
		pysetup_path = os.path.join(os.path.dirname(os.path.dirname(maven.__file__)), 'pysetup')
		result = self.project_manager.define_project_type(path=pysetup_path)
		self.assertEquals(result, 'pysetup')

	def test_define_project_type_undefined(self):
		undefined_path = os.path.join(os.path.dirname(os.path.dirname(maven.__file__)), 'undefined')
		result = self.project_manager.define_project_type(path=undefined_path)
		self.assertEquals(result, 'undefined')