import os
import sys
import config.dep_def
from . import git_dep_updater
from . import url_dep_updater


def update_deps(args, dir, deps):
    for dep in deps:
        print('Process %s...' % os.path.join(dir, dep.PATH))
        if isinstance(dep, config.dep_def.GitDep):
            if not git_dep_updater.GitDepUpdater.update(args, dir, dep):
                return False
        elif isinstance(dep, config.dep_def.UrlDep):
            if not url_dep_updater.UrlDepUpdater.update(args, dir, dep):
                return False
        else:
            return False
