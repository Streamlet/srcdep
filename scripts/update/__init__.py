import config.dep_def
from . import git_dep_updater
from . import url_dep_updater


def update_dep(args, dir, dep):
    if isinstance(dep, config.dep_def.GitDep):
        if not git_dep_updater.GitDepUpdater.update(args, dir, dep):
            return False
    elif isinstance(dep, config.dep_def.UrlDep):
        if not url_dep_updater.UrlDepUpdater.update(args, dir, dep):
            return False
    else:
        return False
    return True
