import os, subprocess, shutil, locale


class GitDepUpdater(object):

    @staticmethod
    def update(args, dir, dep):
        dest = os.path.join(dir, dep.PATH)
        if os.path.exists(dest):
            if args.force:
                print("%s exists, removing..." % dest)
                shutil.rmtree(dest)
            else:
                print("%s exists, skip" % dest)
                return True
        if not cmd('git clone %s %s' % (dep.GIT_REPO, dest)):
            return False
        os.chdir(dest)
        if not cmd('git checkout %s --detach' % dep.GIT_TAG):
            return False
        os.chdir(dir)
        return True


def cmd(cmd):
    print(cmd)
    process = subprocess.Popen(cmd,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,
                               shell=True)
    encoding = locale.getpreferredencoding(False)
    (stdoutdata, stderrdata) = process.communicate()
    if stdoutdata is not None:
        print(stdoutdata.decode())
    if stderrdata is not None:
        print(stderrdata.decode())
    return process.wait() == 0
