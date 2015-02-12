

class UserInfoDomain():
    username = None
    workspaces = []

    def __init__(self, username, workspaces=[]):
        self.username = username
        self.workspaces = workspaces


class WorkspaceDomain():
    workspace = None
    directories = []

    def __init__(self, workspace, directories=[]):
        self.workspace = workspace
        self.directories = directories


class DirectoryDomain():
    git_directory = None
    git_shortname = None
    git_branches = []

    def __init__(self, git_directory, git_shortname, git_branches=[]):
        self.git_directory = git_directory
        self.git_shortname = git_shortname
        self.git_branches = git_branches


class BranchDomain():
    git_branch = None

    def __init__(self, git_branch):
        self.git_branch = git_branch