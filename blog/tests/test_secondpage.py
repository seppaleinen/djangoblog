from django.test import TestCase
from blog.models import Directory
from blog.models import Branch
from blog.models import UserInfo
from blog.models import Workspace
import os


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