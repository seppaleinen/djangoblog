from django.db import models


#Det automatiska tabellnamnet blir paketnamn (database) och class (Directory) med underscore mellan
#t,ex database_directory
#om man inte har class Meta med db_table som manuellt saetter om
class Directory(models.Model):
    git_directory = models.CharField(max_length=100)
    git_shortname = models.CharField(max_length=100)

    @classmethod
    def create(cls, git_directory, git_shortname):
        return cls(git_directory=git_directory, git_shortname=git_shortname)

    class Meta:
        db_table = u'database_directory'


class UserInfo(models.Model):
    username = models.CharField(max_length=100)

    @classmethod
    def create(cls, username):
        return cls(username=username)

    class Meta:
        db_table = u'user_info'


class Workspace(models.Model):
    user_info = models.ForeignKey(UserInfo)
    workspace = models.CharField(max_length=100)

    @classmethod
    def create(cls, user_info=user_info, workspace='main'):
        return cls(user_info=user_info, workspace=workspace)

    class Meta:
        db_table = u'workspace'


class Branch(models.Model):
    directory = models.ForeignKey(Directory)
    git_branch = models.CharField(max_length=100)

    @classmethod
    def create(cls, git_branch, directory):
        return cls(git_branch=git_branch, directory=directory)

    class Meta:
        db_table = u'database_branch'