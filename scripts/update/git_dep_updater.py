import os
import subprocess
import shutil
import locale


class GitDepUpdater(object):

    @staticmethod
    def update(args, dir, dep):
        dest = os.path.join(dir, dep.PATH)
        existed = False
        if os.path.exists(dest):
            if os.path.exists(os.path.join(dest, '.git')) and not args.force:
                existed = True
            else:
                shutil.rmtree(dest)
        if not existed:
            if not cmd('git clone %s %s' % (dep.GIT_REPO, dest)):
                print('Failed to clone %s to %s' % (dep.GIT_REPO, dest))
                return False
        os.chdir(dest)
        if existed:
            if not cmd('git fetch -p -f -t && git fetch -p -f -P && echo Synced remote branches and tags'):
                print('Failed to sync remote branches and tags')
                return False
        if not cmd('git reset %s --hard' % dep.GIT_TAG):
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
