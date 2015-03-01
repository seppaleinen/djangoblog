from blog.models import Directory
from blog.models import Branch
from blog.models import Workspace
from blog.logic.git_manager import get_all_branches


def save_dir_to_database(git_directory, git_shortname, workspace):
    directory = Directory.create(git_directory=git_directory, git_shortname=git_shortname, workspace=workspace)
    directory.save()
    return directory


def get_branches_for_dir_and_save(directory):
    directory.branch_set.all().delete()
    current_branch = None
    result = get_all_branches(directory.git_directory)
    for line in result.stdout.readlines():
        if '*' in line:
            current_branch = line.split('* ')[-1]
        if 'remotes/' in line:
            branch_name = line.split(' ')[2].split('/')[-1].rstrip()
            if 'HEAD' not in branch_name:
                branch = Branch.create(git_branch=branch_name, directory=directory)
                branch.save()


def remove_all_under_workspace(workspace_name):
    workspace_list = Workspace.objects.filter(workspace=workspace_name)
    for workspace in workspace_list:
        directory_list = workspace.directory_set.all()
        for directory in directory_list:
            directory.branch_set.delete()
        directory_list.delete()
    workspace_list.delete()