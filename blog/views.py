import os

from django.shortcuts import render

from blog.models.domain.dir_domain_model import DirDomain
from blog.models.database.dir_db_model import Directory
from blog.models.database.dir_db_model import Branch
from blog.models.database.dir_db_model import UserInfo
from blog.models.database.dir_db_model import Workspace
from blog.models.form.form_model import Form


def home(request):
    return render(request, 'startPage.html')


def username(request):
    workspace = None
    if 'username' in request.POST and request.POST['username']:
        username = request.POST['username']
        user = UserInfo.objects.filter(username=username)
        if user.exists():
            workspace_list = Workspace.objects.filter(user_info=user)
            print('workspaces under', user[0].username)
            for workspac in workspace_list:
                workspace = workspac
                print(workspac.workspace)
                directory_list = Directory.objects.filter(workspace=workspac)
                for directory in directory_list:
                    branch_list = Branch.objects.filter(directory=directory)
                    print('branches under', directory.git_shortname)
                    for branch in branch_list:
                        print(branch.git_branch)
        else:
            print('else')
            new_user = UserInfo.create(username)
            new_user.save()
    dirs = Directory.objects.filter(workspace=workspace)
    return render(request, 'second.html', {'dirs': dirs})



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
    q = None
    if 'input_text' in request.POST and request.POST['input_text']:
        q = request.POST['input_text']
        workspace = Workspace.objects.filter(workspace='main')[0]
        dirs_to_remove = Directory.objects.filter(workspace=workspace)
        for remove_dir in dirs_to_remove:
            remove_dir.delete()

        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(q)
            for f in dirnames if f.endswith('.git')]
        for dir in dirs:
            git_directory=dir
            git_shortname=dir.replace('/.git', '').split('/')[-1]
#            for work in Workspace.objects.filter(workspace='main'):
#                print('workspace: ', work.workspace)
#                for dirr in Directory.objects.filter(workspace=work):
#                    print('deleting', dirr.git_shortname)
            save_dir_to_database(git_directory=git_directory, git_shortname=git_shortname, workspace=workspace)
#            for dirrr in Directory.objects.filter(workspace=workspace):
#                print('found: ', dirrr.git_shortname)

        dirs = Directory.objects.filter(workspace=workspace)
    return render(request, 'second.html', {'dirs': dirs, 'current_workspace': q})


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


def save_dir_to_database(git_directory, git_shortname, workspace):
    directory = Directory.create(git_directory=git_directory, git_shortname=git_shortname, workspace=workspace)
    directory.save()


def test_database():
    Directory.objects.all().delete()
    Branch.objects.all().delete()
    UserInfo.objects.all().delete()
    Workspace.objects.all().delete()
    directory = Directory.create(git_directory='~/hejhej', git_shortname='aelskar jackie')
    directory.save()

    user_info = UserInfo.create(username='seppa')
    user_info.save()
    new_user = UserInfo.objects.filter(username='seppa')[0]
    print('---- user_info ----')
    print(new_user.username)

    branch = Branch.create(git_branch='master', directory=directory)
    branch.save()
    branch_two = Branch.create(git_branch='secondary', directory=directory)
    branch_two.save()
    branches = Branch.objects.filter(directory=directory)
    print('---- branches ----')
    for branc in branches:
        print(branc.directory.git_shortname, branc.git_branch)

    workspace = Workspace.create(user_info=user_info)
    workspace.save()
    workspace_two = Workspace.create(user_info=user_info, workspace='licensansokan')
    workspace_two.save()
    workspaces = Workspace.objects.filter(user_info=user_info)
    print('---- workspace ----')
    for workspac in workspaces:
        print(workspac.workspace, workspac.user_info.username)