import os

from django.shortcuts import render

from blog.models.domain.dir_domain_model import DirDomain
from blog.models.database.dir_db_model import Directory
from blog.models.form.form_model import Form


def home(request):
    all_dirs = Directory.objects.all()
    form = Form()
    if all_dirs.exists():
        return render(request, 'second.html', {'dirs':all_dirs, 'form':form})
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
    if 'input_text' in request.POST and request.POST['input_text']:
        q = request.POST['input_text']
        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(q)
            for f in dirnames if f.endswith('.git')]
        for dir in dirs:
            git_directory=dir
            git_shortname=dir.replace('/.git', '').split('/')[-1]
            found_dirs = Directory.objects.filter(git_shortname=git_shortname)
            save_dir_to_database(directories=found_dirs, git_directory=git_directory, git_shortname=git_shortname)
    return render(request, 'second.html', {'dirs': Directory.objects.all(),
                                           'current_workspace': q})


def hoj(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            print('awwyiss')
            return render(request, "second.html", {'dirs': Directory.objects.all(),
                                                   'current_name': form.cleaned_data['your_name']})
    else:
        form = Form()
    return render(request, "second.html", {'dirs': Directory.objects.all()})


def save_dir_to_database(directories, git_directory, git_shortname):
    if directories.exists():
        directory = directories[0]
        directory.git_directory = git_directory
        directory.git_shortname = git_shortname
    else:
        directory = Directory.create(git_directory=git_directory, git_shortname=git_shortname)
    directory.save()