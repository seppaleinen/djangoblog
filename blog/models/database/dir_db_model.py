from django.db import models


#Det automatiska tabellnamnet blir paketnamn (database) och class (Directory) med underscore mellan
#t,ex database_directory
class Directory(models.Model):
    git_directory = models.CharField(max_length=100)
    git_shortname = models.CharField(max_length=100)

    @classmethod
    def create(cls, git_directory, git_shortname):
        directory = cls(git_directory=git_directory, git_shortname=git_shortname)
        return directory