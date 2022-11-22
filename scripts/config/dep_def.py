import os, sys

DEPS = 'DEPS'
GIT_REPOSITORY = 'GIT_REPOSITORY'
GIT_TAG = 'GIT_TAG'
URL = 'URL'
URL_FORMAT = 'URL_FORMAT'
TAR_GZ = 'tar.gz'
TAR_BZ2 = 'tar.bz2'
if sys.version >= '3':
    TAR_XZ = 'tar.xz'
ZIP = 'zip'
URL_HASH = 'URL_HASH'
MD5 = 'MD5'
SHA1 = 'SHA1'
SHA224 = 'SHA224'
SHA256 = 'SHA256'
SHA384 = 'SHA384'
SHA512 = 'SHA512'
ROOT_DIR = 'ROOT_DIR'


def dict_to_object(dict):
    assert DEPS in dict, 'Root element MUST be "%s"' % DEPS
    deps = []
    for path in dict[DEPS]:
        deps.append(Dep.new(path, dict[DEPS][path]))
    return deps


class Dep(object):
    def __init__(self, path):
        self.PATH = path.replace('/', os.path.sep).replace('\\', os.path.sep)

    @staticmethod
    def new(path, config):
        if GIT_REPOSITORY in config:
            return GitDep(path, config)
        if URL in config:
            return UrlDep(path, config)
        assert False, 'Unsupported dependent type. You MUST specify "%s" or "%s".' % (
            GIT_REPOSITORY, URL)


class GitDep(Dep):
    def __init__(self, path, config):
        super(GitDep, self).__init__(path)
        assert GIT_REPOSITORY in config
        assert GIT_TAG in config, '"%s" MUST be specified in a git dependent'
        self.GIT_REPO = config[GIT_REPOSITORY]
        self.GIT_TAG = config[GIT_TAG]


class UrlDep(Dep):
    def __init__(self, path, config):
        self.URL = None
        self.URL_FORMAT = None
        self.URL_HASH = []
        self.ROOT_DIR = None

        super(UrlDep, self).__init__(path)
        assert URL in config
        self.URL = config[URL]
        if URL_FORMAT in config:
            self.URL_FORMAT = config[URL_FORMAT]
        else:
            filename_part = os.path.basename(self.URL).split('.')
            if len(filename_part) >= 2 and filename_part[-2] == 'tar':
                ext_name = 'tar.' + filename_part[-1]
            else:
                ext_name = filename_part[-1]
            assert ext_name in [
                TAR_GZ, TAR_BZ2, ZIP
            ], 'Supported formats are: %s, %s, %s' % (TAR_GZ, TAR_BZ2, ZIP)
            self.URL_FORMAT = ext_name
        if URL_HASH in config:
            for algo in config[URL_HASH]:
                self.URL_HASH.append(UrlHash(algo, config[URL_HASH][algo]))
        if ROOT_DIR in config:
            self.ROOT_DIR = config[ROOT_DIR]


class UrlHash(object):
    def __init__(self, algo, hash):
        self.ALGORITHM = algo
        self.HASH = hash
