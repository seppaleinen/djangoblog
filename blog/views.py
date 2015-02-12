import os

from django.shortcuts import render

from blog.models.domain.dir_domain_model import DirectoryDomain
from blog.models.domain.dir_domain_model import BranchDomain
from blog.models.domain.dir_domain_model import UserInfoDomain
from blog.models.domain.dir_domain_model import WorkspaceDomain
from blog.models.database.dir_db_model import Directory
from blog.models.database.dir_db_model import Branch
from blog.models.database.dir_db_model import UserInfo
from blog.models.database.dir_db_model import Workspace
from blog.models.form.form_model import Form


def home(request):
    return render(request, 'startPage.html')


def username(request):
    user_object = None
    if 'username' in request.POST and request.POST['username']:
        username = request.POST['username']
        user = UserInfo.objects.filter(username=username)
        if user.exists():
            user_object = map_db_to_domain(username)
        else:
            new_user = UserInfo.create(username)
            new_user.save()
            user_object = UserInfoDomain(username)
    print(user_object.username)
    for workspace in user_object.workspaces:
        print(workspace.workspace)
        for directory in workspace.directories:
            print(directory.git_shortname)
            for branch in directory.git_branches:
                print(branch.git_branch)
    return render(request, 'second.html', {'user': user_object})


def map_db_to_domain(username):
    user_domain = UserInfoDomain
    users = UserInfo.objects.filter(username=username)
    if users.exists():
        user = users[0]
        user_domain.username = user.username
        workspace_list = Workspace.objects.filter(user_info=user)
        workspace_domain_list = []
        for workspace in workspace_list:
            workspace_domain = WorkspaceDomain(workspace.workspace)
            directory_list = Directory.objects.filter(workspace=workspace)
            directory_domain_list = []
            for directory in directory_list:
                directory_domain = DirectoryDomain(directory.git_directory, directory.git_shortname)
                branch_list = Branch.objects.filter(directory=directory)
                branch_domain_list = []
                for branch in branch_list:
                    branch_domain_list.append(BranchDomain(branch.git_branch))

                directory_domain.git_branches = branch_domain_list
                directory_domain_list.append(directory_domain)
            workspace_domain.directories = directory_domain_list
            workspace_domain_list.append(workspace_domain)
        user_domain.workspaces = workspace_domain_list
    return user_domain


def about(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'index.html')


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
            save_dir_to_database(git_directory=git_directory, git_shortname=git_shortname, workspace=workspace)

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