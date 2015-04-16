from django.test import TestCase
from blog.logic.git_manager import get_all_branches
from blog.logic.git_manager import git_check_updates_all_branches
import os

class GitManagerTests(TestCase):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.git')

    def test_get_all_branches(self):
        result = get_all_branches(directory_name=self.base_dir)
        self.assertTrue('master' in line for line in result)

    def test_git_check_updates_all_branches(self):
        result = git_check_updates_all_branches(directory_name=self.base_dir)
        self.assertTrue('(up to date)' in line for line in result)