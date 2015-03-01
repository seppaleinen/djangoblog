from django.test import TestCase
from blog.models import Directory
from blog.models import Branch
from blog.models import UserInfo
from blog.models import Workspace
from blog.logic.git_manager import get_all_branches
from blog.logic.git_manager import git_check_updates_all_branches
import os


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


class DatabaseTest(TestCase):
    def setUp(self):
        self.user_info = UserInfo.create(username='username')
        self.user_info.save()

        self.workspace = Workspace.create(user_info=self.user_info, workspace='main')
        self.workspace.save()

        self.directory = Directory.create(git_directory='pathname', git_shortname='name', workspace=self.workspace)
        self.directory.save()

        self.branch = Branch.create(git_branch='master', directory=self.directory)
        self.branch.save()

    def test_create_user_and_load(self):
        db_user_info = UserInfo.objects.get(username='username')
        self.assertTrue(db_user_info)
        self.assertEqual(db_user_info.username, 'username')

        db_workspace = Workspace.objects.get(workspace='main')
        self.assertTrue(db_workspace)
        self.assertEqual(db_workspace.workspace, 'main')

        db_directory = Directory.objects.get(git_shortname='name')
        self.assertTrue(db_directory)
        self.assertEqual(db_directory.git_directory, 'pathname')

        db_branch = Branch.objects.get(git_branch='master')
        self.assertTrue(db_branch)
        self.assertEqual(db_branch.git_branch, 'master')

    def test_reverse_lookup_from_user_info(self):
        #Get userinfo model and reverse lookup the tree
        db_user_info = UserInfo.objects.get(username=self.user_info.username)
        self.assertTrue(db_user_info)
        db_workspace_list = db_user_info.workspace_set.all()
        self.assertTrue(db_workspace_list)
        self.assertGreater(db_workspace_list.count(), 0)
        for db_workspace in db_workspace_list:
            db_directory_list = db_workspace.directory_set.all()
            self.assertTrue(db_directory_list)
            self.assertGreater(db_directory_list.count(), 0)
            for db_directory in db_directory_list:
                db_branch_list = db_directory.branch_set.all()
                self.assertTrue(db_branch_list)
                self.assertGreater(db_branch_list.count(), 0)
                for db_branch in db_branch_list:
                    self.assertTrue(db_branch)


class StartPageTests(TestCase):
    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_page_contains(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="your_name"')


class SecondPageTests(TestCase):
    def setUp(self):
        user_info = UserInfo.create(username='user')
        user_info.save()
        workspace = Workspace.create(user_info=user_info, workspace='workspace_name')
        workspace.save()
        directory = Directory.create(git_directory='pathname', git_shortname='git_branch_name', workspace=workspace)
        directory.save()
        branch = Branch.create(git_branch='branch_name', directory=directory)
        branch.save()

    def test_homepage(self):
        response = self.client.post('/username/', {'username':'user'})
        self.assertEqual(response.status_code, 200)

    def test_page_contains(self):
        response = self.client.post('/username/', {'username':'user'})
        self.assertContains(response, 'Directory to workspace:')
        self.assertContains(response, 'user')
        self.assertContains(response, 'workspace_name')
        self.assertContains(response, 'git_branch_name')
        self.assertContains(response, 'branch_name')


class GitManagerTests(TestCase):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.git')

    def test_get_all_branches(self):
        result = get_all_branches(directory_name=self.base_dir)
        self.assertTrue('master' in line for line in result)

    def test_git_check_updates_all_branches(self):
        result = git_check_updates_all_branches(directory_name=self.base_dir)
        self.assertTrue('(up to date)' in line for line in result)