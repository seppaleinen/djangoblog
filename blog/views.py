from django.shortcuts import render
from blog.newmodel import posts
import os

def home(request):
    if 'inputtext' in request.POST and request.POST['inputtext']:
        q = request.POST['inputtext']
        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(q)
            for f in dirnames if f.endswith('.git')]

    return render(request, 'second.html', {'dirs':dirs})


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
    entries = []
    if 'inputtext' in request.POST and request.POST['inputtext']:
        q = request.POST['inputtext']
        entries = [{'author': q, 'title': 'other title', 'bodytext': 'other bodytext', 'timestamp': 'other timestamp'}]
    if 'inputtext' in request.GET and request.GET['inputtext']:
        q = request.GET['inputtext']
        entries = [{'author': q, 'title': 'other title', 'bodytext': 'other bodytext', 'timestamp': 'other timestamp'}]

    return render(request, 'index.html', {'posts': entries})