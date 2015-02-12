"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from blog.models.database.dir_db_model import Directory
from blog.models.database.dir_db_model import Branch
from blog.models.database.dir_db_model import UserInfo
from blog.models.database.dir_db_model import Workspace


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)


class DatabaseTest(TestCase):
    def test_create_user_and_load(self):
        directory = Directory.create(git_directory='/Users/seppa/workspace', git_shortname='workspace')
        directory.save()
        loaded_directory = Directory.objects.filter(git_shortname='workspace')[0]
        self.assertIsNotNone(loaded_directory, 'loaded_directory should not be None')
        self.assertEqual(loaded_directory.git_directory, '/Users/seppa/workspace', 'git_directory should be equals')