from django.test import TestCase
from blog.logic.git_manager import get_all_branches
from blog.logic.git_manager import git_check_updates_all_branches
from blog.logic.git_manager import checkout_to_branch
from blog.logic.git_manager import git_pull
from blog import views
import os

class GitManagerTests(TestCase):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(views.__file__)), '.git')

    def test_get_all_branches(self):
        result = get_all_branches(directory_name=self.base_dir)
        self.assertTrue('master' in line for line in result)

    def test_git_check_updates_all_branches(self):
        result = git_check_updates_all_branches(directory_name=self.base_dir)
        self.assertTrue('(up to date)' in line for line in result)

    def test_git_checkout_to_branch(self):
    	results = get_all_branches(directory_name=self.base_dir)
    	current_branch = None
    	for result in results:
    		if '*' in result:
    			current_branch = result.replace('* ', '').replace('\n','')
    	self.assertIsNotNone(current_branch)
    	checkout_result = checkout_to_branch(directory_name=self.base_dir, branch_name=current_branch)
    	self.assertIn(current_branch, checkout_result[0])

    def test_git_pull(self):
    	results = get_all_branches(directory_name=self.base_dir)
    	current_branch = None
    	for result in results:
    		if '*' in result:
    			current_branch = result.replace('* ', '').replace('\n', '')

    	self.assertIsNotNone(current_branch)
    	git_pull_result = git_pull(directory_name=self.base_dir, branch_name=current_branch)
    	self.assertIsNotNone(git_pull_result)
