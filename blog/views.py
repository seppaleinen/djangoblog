import os

from django.shortcuts import render

from blog.models.domain.dir_domain_model import DirDomain


def home(request):
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