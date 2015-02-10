from django.shortcuts import render
from blog.models import posts
from blog.newmodel import posts

def home(request):
    #entries = posts.objects.all()[:10]
    entries = []
    for i in range(3):
        entries.append(posts)
    return render(request, 'index.html', {'posts' : entries})

def about(request):
    #entries = posts.objects.all()[:10]
    entries = []
    for i in range(2):
        entries.append(posts)
    return render(request, 'index.html', {'posts' : entries})

def contact(request):
    #entries = posts.objects.all()[:10]
    entries = []
    for i in range(4):
        entries.append(posts)
    return render(request, 'index.html', {'posts' : entries})

def input(request):
    entries = []
    if 'inputtext' in request.POST and request.POST['inputtext']:
        q = request.POST['inputtext']
        entries = [{'author' : q, 'title' : 'other title', 'bodytext' : 'other bodytext', 'timestamp' : 'other timestamp'}]
    if 'inputtext' in request.GET and request.GET['inputtext']:
        q = request.GET['inputtext']
        entries = [{'author' : q, 'title' : 'other title', 'bodytext' : 'other bodytext', 'timestamp' : 'other timestamp'}]

    return render(request, 'index.html', {'posts' : entries})