import os

from django.shortcuts import render

from blog.models.domain.dir_domain_model import DirDomain
from blog.models.database.dir_db_model import Posts


def home(request):
    save_to_database()
    load_singular_from_database()
    load_multiple_from_database()
    env_workspace = os.getenv('WORKSPACE', "~/")
    if env_workspace:
        dirs = [DirDomain(directory=os.path.join(dirpath, f))
            for dirpath, dirnames, files in os.walk(env_workspace)
            for f in dirnames if f.endswith('.git')]
        return render(request, 'index.html', {'dirs':dirs})
    else:
        return render(request, 'second.html')


def about(request):
    entries = []
    for i in range(2):
        dir_domain = DirDomain(directory="~/Downloads")
        entries.append(dir_domain)
    return render(request, 'index.html', {'dirs': entries})


def contact(request):
    entries = []
    for i in range(4):
        dir_domain = DirDomain(directory="~/Downloads")
        entries.append(dir_domain)
    return render(request, 'index.html', {'dirs': entries})


def input(request):
    dirs = []
    if 'inputtext' in request.POST and request.POST['inputtext']:
        q = request.POST['inputtext']
        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(q)
            for f in dirnames if f.endswith('.git')]

    return render(request, 'index.html', {'dirs': dirs})


def save_to_database():
    post = Posts.create(author="authorz", title="Title", bodytext="Bodytext3", timestamp="1986-07-02 12:43")
    post.save()


#objects.get kan bara hantera resultset med 1
def load_singular_from_database():
    posts = Posts.objects.get(author="david")
    print(posts.bodytext)


#objects.filter ger tillbaks en lista med resultat
def load_multiple_from_database():
    posts = Posts.objects.filter(author="authorz")
    for post in posts:
        print(post.bodytext)