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
                # print("%s exists, removing..." % dest)
                shutil.rmtree(dest)
            else:
                # print("%s exists" % dest)
                cloned = False
        if cloned:
            if not cmd('git clone %s %s' % (dep.GIT_REPO, dest)):
                return False
        os.chdir(dest)
        if not cloned:
            if not cmd('git fetch -p -t && git fetch -p -P && echo Synced remote branches and tags'):
                return False
            if cmd('git show-ref -q --verify refs/heads/%s' % dep.GIT_TAG):
                if not cmd('git checkout HEAD --detach'):
                    return False
                if not cmd('git reset --hard'):
                    return False
                if not cmd('git branch -D %s' % dep.GIT_TAG):
                    return False
        if not cmd('git checkout %s' % dep.GIT_TAG):
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
