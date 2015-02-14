import os

from django.shortcuts import render
import subprocess

from blog.models.database.dir_db_model import Directory
from blog.models.database.dir_db_model import Branch
from blog.models.database.dir_db_model import UserInfo
from blog.models.database.dir_db_model import Workspace
from blog.models.form.form_model import Form


def home(request):
    return render(request, 'startPage.html')


#TODO Undersok om det gar att fa in db_modellerna som json-komprimerade
#TODO listor i textfalt i userInfo istallet for separata tabeller
def username(request):
    users = None
    if 'username' in request.POST and request.POST['username']:
        username = request.POST['username']
        users = UserInfo.objects.filter(username=username)
        if not users.exists():
            users = UserInfo.create(username)
            users.save()
    return render(request, 'second.html', {'users': users})


def add_workspace(request):
    users = []
    if 'workspace_name' in request.POST and request.POST['workspace_name']:
        workspace_name = request.POST['workspace_name']
        if 'username' in request.POST and request.POST['username']:
            username = request.POST['username']
            user = UserInfo.objects.get(username=username)
            users.append(user)
            workspace = Workspace.create(user, workspace_name)
            workspace.save()

    return render(request, 'second.html', {'users': users})


def remove_workspace(request):
    if 'workspace_name' in request.POST and request.POST['workspace_name']:
        print('workspace')
        workspace_name = request.POST['workspace_name']
        workspace_list = Workspace.objects.filter(workspace=workspace_name)
        for workspace in workspace_list:
            print("deleting %s" % workspace.workspace)
            directory_list = workspace.directory_set.all()
            for directory in directory_list:
                print(directory)
                directory.branch_set.delete()
            directory_list.delete()
        workspace_list.delete()

    if 'username' in request.POST and request.POST['username']:
        print("username %s" % request.POST['username'])
        users = UserInfo.objects.filter(username=request.POST['username'])
        return render(request, 'second.html', {'users': users})
    else:
        return render(request, 'startPage.html')



def about(request):
    return render(request, 'index.html')


def contact(request):
    return render(request, 'index.html')


def input(request):
    users = []
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
            directory = save_dir_to_database(git_directory=git_directory, git_shortname=git_shortname, workspace=workspace)
            get_branches_for_dir_and_save(directory)

    if 'username' in request.POST and request.POST['username']:
        username = request.POST['username']
        users = UserInfo.objects.filter(username=username)
    return render(request, 'second.html', {'users': users})


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


def get_branches_for_dir_and_save(directory):
    current_branch = None
    git_work_tree = directory.git_directory.replace('/.git', '')
    git_dir = directory.git_directory
    git_command = "git --git-dir=%s --work-tree=%s branch -a" % (git_dir, git_work_tree)
    result = subprocess.Popen(git_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in result.stdout.readlines():
        if '*' in line:
            current_branch = line.split('* ')[-1]
        if 'remotes/' in line:
            branch = line.split(' ')[2].split('/')[-1].rstrip()
            if not Branch.objects.filter(git_branch=branch, directory=directory).exists():
                branch = Branch.create(git_branch=branch, directory=directory)
                branch.save()


def save_dir_to_database(git_directory, git_shortname, workspace):
    directory = Directory.create(git_directory=git_directory, git_shortname=git_shortname, workspace=workspace)
    directory.save()
    return directory


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