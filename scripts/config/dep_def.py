import os
import sys

DEPS = 'DEPS'
GIT_REPO = 'GIT_REPO'
GIT_TAG = 'GIT_TAG'
URL = 'URL'
URL_FORMAT = 'URL_FORMAT'
TAR_GZ = 'tar.gz'
TAR_BZ2 = 'tar.bz2'
if sys.version >= '3':
    TAR_XZ = 'tar.xz'
ZIP = 'zip'
SUPPORTED_FORMATS = (TAR_GZ, TAR_BZ2, TAR_XZ,
                     ZIP) if sys.version >= '3' else (TAR_GZ, TAR_BZ2, ZIP)
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


def platform_config(config):
    if isinstance(config, dict) and sys.platform in config:
        return config[sys.platform]
    return config


class Dep(object):
    def __init__(self, path):
        self.PATH = path.replace('/', os.path.sep).replace('\\', os.path.sep)

    @staticmethod
    def new(path, config):
        if GIT_REPO in config:
            return GitDep(path, config)
        if URL in config:
            return UrlDep(path, config)
        assert False, 'Unsupported dependent type. You MUST specify "%s" or "%s".' % (
            GIT_REPO, URL)


class GitDep(Dep):
    def __init__(self, path, config):
        super(GitDep, self).__init__(path)
        assert GIT_REPO in config
        assert GIT_TAG in config, '"%s" MUST be specified in a git dependent'
        self.GIT_REPO = platform_config(config[GIT_REPO])
        assert isinstance(self.GIT_REPO, str), 'GIT_REPO MUST be string'
        self.GIT_TAG = platform_config(config[GIT_TAG])
        assert isinstance(self.GIT_TAG, str), 'GIT_TAG MUST be string'


class UrlDep(Dep):
    def __init__(self, path, config):
        self.URL = None
        self.URL_FORMAT = None
        self.URL_HASH = []
        self.ROOT_DIR = None

        super(UrlDep, self).__init__(path)
        assert URL in config
        self.URL = platform_config(config[URL])
        assert isinstance(self.URL, str), 'URL MUST be string'
        if URL_FORMAT in config:
            self.URL_FORMAT = platform_config(config[URL_FORMAT])
        else:
            filename_part = os.path.basename(self.URL).split('.')
            if len(filename_part) >= 2 and filename_part[-2] == 'tar':
                ext_name = 'tar.' + filename_part[-1]
            else:
                ext_name = filename_part[-1]
            assert ext_name in SUPPORTED_FORMATS, 'File format "%s" not supported, expects %s' % (
                ext_name, ', '.join(SUPPORTED_FORMATS))
            self.URL_FORMAT = ext_name
        assert isinstance(self.URL_FORMAT, str), 'URL_FORMAT MUST be string'
        if URL_HASH in config:
            for algo in config[URL_HASH]:
                self.URL_HASH.append(
                    UrlHash(algo, platform_config(config[URL_HASH][algo])))
        if ROOT_DIR in config:
            self.ROOT_DIR = platform_config(config[ROOT_DIR])
            assert isinstance(self.ROOT_DIR, str), 'ROOT_DIR MUST be string'


class UrlHash(object):
    def __init__(self, algo, hash):
        self.ALGORITHM = algo
        self.HASH = hash
        assert isinstance(self.HASH, str), 'URL_HASH value MUST be string'
