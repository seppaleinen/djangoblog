import os


class ProjectManager(object):
    def search_dir_for_projects(self, path):
        dirs = [os.path.join(dirpath, f)
            for dirpath, dirnames, files in os.walk(path)
            for f in dirnames if f.endswith('.git') and files is not None]
        return dirs

    def define_project_type(self, path):
        for item in os.listdir(path):
            if os.path.isfile(os.path.join(path, item)):
                if 'manage.py' in item:
                    return 'django'
                if 'pom.xml' in item:
                    return 'maven'
                if 'setup.py' in item:
                    return 'pysetup'
                if 'build.gradle' in item:
                    return 'gradle'
        return 'undefined'