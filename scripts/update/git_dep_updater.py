import os, subprocess

class GitDepUpdater(object):
    @staticmethod
    def update(args, dir, dep):
        dest = os.path.join(dir, dep.PATH)
        if os.path.exists(dest):
            return
        cmd('git clone %s %s' %(dep.GIT_REPO, dest))
        os.chdir(dest)
        cmd('git fetch')
        cmd('git reset --hard')
        cmd('git checkout %s --detach' % dep.GIT_TAG)
        os.chdir(dir)


def cmd(cmd):
    print(cmd)
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    (stdoutdata, stderrdata) = process.communicate()
    if stdoutdata is not None:
        print(stdoutdata)
    if stderrdata is not None:
        print(stderrdata)
    return process.wait()
