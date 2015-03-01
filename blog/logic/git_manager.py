import subprocess


def get_all_branches(directory_name):
    """
    Runs "git branch -a" and returns result
    :param directory_name:
    :return:
    """
    git_arg = "branch -a"
    return __do_git_command__(directory_name=directory_name, git_arg=git_arg)


def checkout_to_branch(directory_name, branch_name):
    """
    Runs "git checkout %branch_name" and returns result
    :param directory_name:
    :param branch_name:
    :return:
    """
    git_arg = "checkout %s" % branch_name
    return __do_git_command__(directory_name=directory_name, git_arg=git_arg)


def git_pull(directory_name, branch_name):
    """
    Runs git checkout %branch_name and then git pull and returns result
    :param directory_name:
    :param branch_name:
    :return:
    """
    checkout_to_branch(directory_name=directory_name, branch_name=branch_name)
    git_arg = "pull"
    return __do_git_command__(directory_name=directory_name, git_arg=git_arg)


def git_check_updates_all_branches(directory_name):
    """
    Runs git remote show origin and returns result
    :param directory_name:
    :return:
    """
    git_arg = "remote show origin"
    return __do_git_command__(directory_name=directory_name, git_arg=git_arg)


def __do_git_command__(directory_name, git_arg):
    """
    returns result of git command as list of strings
    :param directory_name:
    :param git_arg:
    :return:
    """
    git_work_tree = directory_name.replace('/.git', '')
    git_command = "git --git-dir=%s --work-tree=%s %s" % (directory_name, git_work_tree, git_arg)
    return subprocess.Popen(git_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout.readlines()