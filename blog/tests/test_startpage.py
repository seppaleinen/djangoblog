from django.test import TestCase
from blog.models import Directory
from blog.models import Branch
from blog.models import UserInfo
from blog.models import Workspace
import os


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