from django.shortcuts import render_to_response
from blog.models import posts
from blog.newmodel import posts

def home(request):
    #entries = posts.objects.all()[:10]
    entries = []
    for i in range(10):
        entries.append(posts)
    return render_to_response('index.html', {'posts' : entries})

def home2(request):
    #entries = posts.objects.all()[:10]
    entries = []
    for i in range(2):
        entries.append(posts)
    return render_to_response('index.html', {'posts' : entries})