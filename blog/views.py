import os

from django.shortcuts import render

from blog.models.domain.dir_domain_model import DirDomain
from blog.models.database.dir_db_model import Directory


def home(request):
    print('before db')
    all_dirs = Directory.objects.all()
    print('after db')
    if all_dirs.exists():
        print('if')
        return render(request, 'second.html', {'dirs':all_dirs})
    else:
        print('else')
        return render(request, 'second.html')
    print('after')
    #env_workspace = os.getenv('WORKSPACE', "~/")
    #if env_workspace:
    #    dirs = [DirDomain(directory=os.path.join(dirpath, f))
    #        for dirpath, dirnames, files in os.walk(env_workspace)
    #        for f in dirnames if f.endswith('.git')]
    #    return render(request, 'second.html', {'dirs':dirs})
    #else:
    #    return render(request, 'second.html')


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
            print(git_directory, git_shortname)
            found_dirs = Directory.objects.filter(git_shortname=git_shortname)
            if found_dirs.exists():
                found_dir = found_dirs[0]
                found_dir.git_directory(git_directory)
                found_dir.git_shortname(git_shortname)
                found_dir.save()
            else:
                new_dir = Directory.create(git_directory=git_directory, git_shortname=git_shortname)
                new_dir.save()
    return render(request, 'second.html', {'dirs': dirs})


def save_to_database():
    dir = Directory.create(git_directory="/Users/shaman_king_2000/IdeaProjects/djangoblog/.git", git_shortname="djangoblog")
    dir.save()


#objects.get kan bara hantera resultset med 1
def load_singular_from_database():
    dir = Directory.objects.get(git_shortname="djangoblog")
    print(dir.git_directory)


#objects.filter ger tillbaks en lista med resultat
def load_multiple_from_database():
    dirs = Directory.objects.filter(git_directory="/Users/shaman_king_2000/IdeaProjects/djangoblog/.git")
    for dir in dirs:
        print(dir.git_shortname)