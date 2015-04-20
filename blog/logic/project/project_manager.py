import os


class ProjectManager(object):
    def search_dir_for_projects(self, path):
        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(path)
            for f in dirnames if f.endswith('.git') and files is not None]
        return dirs