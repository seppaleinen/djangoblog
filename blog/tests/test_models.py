from django.test import TestCase
from blog.models import Directory
from blog.models import Branch
from blog.models import UserInfo
from blog.models import Workspace

class ModelsMetaTest(TestCase):
    def test_user_info_meta_info(self):
        self.assertEqual(str(UserInfo._meta.verbose_name_plural), "user_info_list")
        self.assertEqual(str(UserInfo._meta.db_table), 'user_info')

    def test_workspace_meta_info(self):
        self.assertEqual(str(Workspace._meta.verbose_name_plural), "workspace_list")
        self.assertEqual(str(Workspace._meta.db_table), 'workspace')

    def test_directory_meta_info(self):
        self.assertEqual(str(Directory._meta.verbose_name_plural), "directory_list")
        self.assertEqual(str(Directory._meta.db_table), 'database_directory')

    def test_branch_meta_info(self):
        self.assertEqual(str(Branch._meta.verbose_name_plural), "branch_list")
        self.assertEqual(str(Branch._meta.db_table), 'database_branch')