from django.test import TestCase
from blog.models import Directory
from blog.models import Branch
from blog.models import UserInfo
from blog.models import Workspace
from blog.logic.database_manager import save_dir_to_database
from blog.logic.database_manager import get_branches_for_dir_and_save
from blog.logic.database_manager import remove_all_under_workspace
from blog import views
import os

class DatabaseManagerTests(TestCase):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(views.__file__)), '.git')

        self.user_info = UserInfo.create(username='username')
        self.user_info.save()

        self.workspace = Workspace.create(user_info=self.user_info, workspace='main')
        self.workspace.save()

        self.directory = Directory.create(git_directory=self.base_dir, git_shortname='name', workspace=self.workspace)
        self.directory.save()

        self.branch = Branch.create(git_branch='branch_name', directory=self.directory)
        self.branch.save()

    def test_save_dir_to_database(self):
        git_directory='/Users/shaman_king_2000/IdeaProjects/djangoblog/.git'
        git_shortname='djangoblog'
        saved_dir = save_dir_to_database(
            git_directory=git_directory, 
            git_shortname=git_shortname,
            workspace=self.workspace)

        db_dir = Directory.objects.get(git_shortname='djangoblog')
        self.assertIsNotNone(db_dir)

    def test_get_branches_for_dir_and_save(self):
        db_branch_before = Branch.objects.get(git_branch='branch_name')
        self.assertIsNotNone(db_branch_before)

        get_branches_for_dir_and_save(self.directory)
        db_directory_after = Directory.objects.get(git_directory=self.base_dir)
        self.assertIsNotNone(db_directory_after)
        branch_list = db_directory_after.branch_set.all()
        found = False
        for branch in branch_list:
            found = 'master' in branch.git_branch
        self.assertTrue(found)

    def test_remove_all_under_workspace(self):
        remove_all_under_workspace(self.workspace.workspace)

        self.assertFalse(Branch.objects.filter(git_branch=self.branch.git_branch))
        self.assertFalse(Directory.objects.filter(git_shortname=self.directory.git_shortname))
        self.assertFalse(Workspace.objects.filter(workspace=self.workspace.workspace))