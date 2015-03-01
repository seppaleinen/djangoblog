import subprocess


def get_all_branches(directory_name):
    git_arg="branch -a"
    return __do_git_command__(directory_name=directory_name, git_arg=git_arg)


def checkout_to_branch(directory_name, branch_name):
    git_arg = "checkout %s" % branch_name
    return __do_git_command__(directory_name=directory_name, git_arg=git_arg)


def __do_git_command__(directory_name, git_arg):
    git_work_tree = directory_name.replace('/.git', '')
    git_command = "git --git-dir=%s --work-tree=%s %s" % (directory_name, git_work_tree, git_arg)
    return subprocess.Popen(git_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)