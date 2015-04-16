from django.test import TestCase
from blog.models import Directory
from blog.models import Branch
from blog.models import UserInfo
from blog.models import Workspace

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