from django.shortcuts import render
from blog.newmodel import posts
import os


def home(request):
    env_workspace = os.getenv('WORKSPACE', "~/")
    if env_workspace:
        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(env_workspace)
            for f in dirnames if f.endswith('.git')]
        return render(request, 'index.html', {'dirs':dirs})
    else:
        return render(request, 'second.html')


def about(request):
    entries = []
    for i in range(2):
        entries.append(posts)
    return render(request, 'index.html', {'posts': entries})


def contact(request):
    entries = []
    for i in range(4):
        entries.append(posts)
    return render(request, 'index.html', {'posts': entries})


def input(request):
    dirs = []
    if 'inputtext' in request.POST and request.POST['inputtext']:
        q = request.POST['inputtext']
        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(q)
            for f in dirnames if f.endswith('.git')]

    return render(request, 'index.html', {'dirs': dirs})