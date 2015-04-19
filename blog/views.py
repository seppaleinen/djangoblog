import os

from django.shortcuts import render

from blog.models import Directory
from blog.models import UserInfo
from blog.models import Workspace
from blog.form_model import Form
from blog.logic.database_manager import get_branches_for_dir_and_save
from blog.logic.database_manager import save_dir_to_database
from blog.logic.database_manager import remove_all_under_workspace


def home(request):
    if 'username' in request.POST and request.POST['username']:
        username = request.POST['username']
        users = UserInfo.objects.filter(username=username)
        return render(request, 'second.html', {'users' : users})
    else:
        return render(request, 'startPage.html')


def username(request):
    users = None
    if 'username' in request.POST and request.POST['username']:
        username = request.POST['username']
        users = UserInfo.objects.filter(username=username)
        if not users.exists():
            user = UserInfo.create(username)
            user.save()
            users = UserInfo.objects.filter(username=username)
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
        workspace_name = request.POST['workspace_name']
        remove_all_under_workspace(workspace_name=workspace_name)
    if 'username' in request.POST and request.POST['username']:
        users = UserInfo.objects.filter(username=request.POST['username'])
        return render(request, 'second.html', {'users': users})
    else:
        return render(request, 'startPage.html')


def about(request):
    return render(request, 'index.html')


def testloop(request):
    if 'submit' in request.POST and request.POST['submit']:
        value = request.POST['submit']
        selected_value = request.POST[value.split(' ')[1]]
        print(selected_value)
    return render(request, "second.html", {'users':UserInfo.objects.filter(username='seppa')})


def contact(request):
    return render(request, 'index.html')


def input_view(request):
    if 'input_text' in request.POST and request.POST['input_text']:
        q = request.POST['input_text']
        remove_all_under_workspace('main')

        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(q)
            for f in dirnames if f.endswith('.git') and files is not None]
        for dir_name in dirs:
            git_directory=dir_name
            git_shortname=dir_name.replace('/.git', '').split('/')[-1]
            directory = save_dir_to_database(git_directory=git_directory, git_shortname=git_shortname, workspace=workspace)
            get_branches_for_dir_and_save(directory)

    if 'username' in request.POST and request.POST['username']:
        users = UserInfo.objects.filter(username=request.POST['username'])
    return render(request, 'second.html', {'users': users})


def hoj(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            print('awwyiss')
            return render(request, "second.html", {'dirs': Directory.objects.all(),
                                                   'current_name': form.cleaned_data['your_name']})
    else:
        form = Form(request.POST)
    return render(request, "second.html", {'dirs': Directory.objects.all()})


def testform(request):
    if request.method == 'POST':
        form = Form(request.POST)
        if form.is_valid():
            print('select %s' % form.cleaned_data.get('select'))
    else:
        branches = []
        branches.append(('MAS', 'MAS'))
        branches.append(('SEC', 'SEC'))
        form = Form(tuple(branches))
    return render(request, "index.html", {'form': form})