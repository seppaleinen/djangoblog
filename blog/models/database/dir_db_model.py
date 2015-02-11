from django.db import models


#Det automatiska tabellnamnet blir paketnamn (database) och class (Posts) med underscore mellan
#t,ex database_posts
class Posts(models.Model):
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    bodytext = models.TextField()
    timestamp = models.DateTimeField()

    @classmethod
    def create(cls, author, title, bodytext, timestamp):
        posts = cls(author=author, title=title, bodytext=bodytext, timestamp=timestamp)
        return posts