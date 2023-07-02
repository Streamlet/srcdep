import os
import subprocess
import shutil
import locale


class GitDepUpdater(object):

    @staticmethod
    def update(args, dir, dep):
        dest = os.path.join(dir, dep.PATH)
        cloned = True
        if os.path.exists(dest):
            if args.force:
                shutil.rmtree(dest)
            else:
                cloned = False
        if cloned:
            if not cmd('git clone %s %s' % (dep.GIT_REPO, dest)):
                print('Failed to clone %s to %s' % (dep.GIT_REPO, dest))
                return False
        os.chdir(dest)
        if not cloned:
            if not cmd('git fetch -p -t && git fetch -p -P && echo Synced remote branches and tags'):
                print('Failed to sync remote branches and tags')
                return False
            if cmd('git show-ref -q --verify refs/heads/%s' % dep.GIT_TAG):
                if not cmd('git checkout HEAD --detach'):
                    print('Failed to check out HEAD')
                    return False
                if not cmd('git reset --hard'):
                    print('Failed to reset work space')
                    return False
                if not cmd('git branch -D %s' % dep.GIT_TAG):
                    print('Failed to delete local branch %s' % dep.GIT_TAG)
                    return False
        if not cmd('git checkout %s' % dep.GIT_TAG):
            print('Failed to checkout %s' % dep.GIT_TAG)
            return False
        os.chdir('..')
        return True


def cmd(cmd):
    # print(cmd)
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True)
    encoding = locale.getpreferredencoding(False)
    (stdoutdata, stderrdata) = process.communicate()
    encoding = locale.getpreferredencoding(False)
    # if stdoutdata is not None:
    #     print(stdoutdata.decode(encoding))
    # if stderrdata is not None:
    #     print(stderrdata.decode(encoding))
    return process.wait() == 0
