from django.test import TestCase
from blog.models import Directory
from blog.models import Branch
from blog.models import UserInfo
from blog.models import Workspace
from blog.logic.git_manager import get_all_branches
from blog.logic.git_manager import git_check_updates_all_branches
from blog.logic.database_manager import save_dir_to_database
from blog.logic.database_manager import get_branches_for_dir_and_save
from blog.logic.database_manager import remove_all_under_workspace
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
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.git')

        self.user_info = UserInfo.create(username='username')
        self.user_info.save()

        self.workspace = Workspace.create(user_info=self.user_info, workspace='main')
        self.workspace.save()

        self.directory = Directory.create(git_directory=self.base_dir, git_shortname='name', workspace=self.workspace)
        self.directory.save()

        self.branch = Branch.create(git_branch='branch_name', directory=self.directory)
        self.branch.save()

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_page_contains(self):
        response = self.client.get('/')
        self.assertContains(response, 'id="your_name"')

    def test_post_homepage(self):
        response = self.client.post('/', {'username': self.user_info.username})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.branch.git_branch)



class SecondPageTests(TestCase):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.git')

        user_info = UserInfo.create(username='user')
        user_info.save()
        self.user_info = user_info
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

    def test_username_user_not_exist(self):
        UserInfo.objects.filter(username=self.user_info.username).delete()
        self.assertFalse(UserInfo.objects.filter(username=self.user_info.username))
        
        response = self.client.post('/username/', {'username': 'user'})
        self.assertIsNotNone(UserInfo.objects.filter(username=self.user_info.username))
        self.assertEqual(response.status_code, 200)

    def test_add_workspace(self):
        response = self.client.post('/add/workspace/', 
            {'username': self.user_info.username, 
            'workspace_name': 'secondary'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'secondary')

    def test_remove_workspace_with_username(self):
        response = self.client.post('/remove/workspace/',
            {'username': self.user_info.username,
            'workspace_name': 'workspace_name'})
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Workspace.objects.filter(workspace='workspace_name'))

    def test_remove_workspace_without_username(self):
        response = self.client.post('/remove/workspace/',
            {'workspace_name': 'workspace_name'})
        self.assertEqual(response.status_code, 200)

    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get('/contact')
        self.assertEqual(response.status_code, 200)

    def test_input(self):
        Workspace.create(user_info=self.user_info, workspace='main').save()
        workspace = self.base_dir.replace('djangoblog/.git', '')
        response = self.client.post('/input/', 
            {"input_text": workspace, "username": "user"})
        self.assertEqual(response.status_code, 200)


class GitManagerTests(TestCase):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.git')

    def test_get_all_branches(self):
        result = get_all_branches(directory_name=self.base_dir)
        self.assertTrue('master' in line for line in result)

    def test_git_check_updates_all_branches(self):
        result = git_check_updates_all_branches(directory_name=self.base_dir)
        self.assertTrue('(up to date)' in line for line in result)


class DatabaseManagerTests(TestCase):
    def setUp(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.git')

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