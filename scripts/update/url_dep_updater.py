import os, sys, shutil
from . import hash_algo
from . import package_extractor
if sys.version >= '3':
    import urllib.request as urllib
else:
    import urllib

CACHE_DIR = '.srcdep'


class UrlDepUpdater(object):

    @staticmethod
    def update(args, dir, dep):
        cache_file = os.path.join(
            dir, CACHE_DIR,
            dep.PATH.replace(os.path.sep, '_') + '.' + dep.URL_FORMAT)
        file_changed = False
        if os.path.exists(cache_file) and not verify(cache_file, dep.URL_HASH):
            os.remove(cache_file)
        if not os.path.exists(cache_file):
            # print('Downloading %s ...' % dep.URL)
            if not download(dep.URL, cache_file):
                print('Download %s error' % dep.URL)
                return False
            if not verify(cache_file, dep.URL_HASH):
                print('File %s verified error, stop' % cache_file)
                return False
            file_changed = True

        dest = os.path.join(dir, dep.PATH)
        if os.path.exists(dest):
            if args.force or file_changed:
                # print("%s exists, removing..." % dest)
                shutil.rmtree(dest)
            else:
                # print("%s exists, skip" % dest)
                return True

        extract_dir = dest
        if dep.ROOT_DIR is not None:
            extract_dir = os.path.dirname(extract_dir)
        package_extractor.extract(cache_file, dep.URL_FORMAT, extract_dir)
        if dep.ROOT_DIR is not None:
            os.rename(os.path.join(extract_dir, dep.ROOT_DIR), dest)


def verify(file, url_hashes):
    for url_hash in url_hashes:
        if not hash_algo.verify(file, url_hash.ALGORITHM, url_hash.HASH):
            return False
    return True


def download(url, file):
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    try:
        remote = urllib.urlopen(url)
    except Exception as e:
        print(e)
        return False
    with open(file, 'wb') as local:
        BLOCK_SIZE = 1024 * 1024
        while True:
            buffer = remote.read(BLOCK_SIZE)
            local.write(buffer)
            if len(buffer) < BLOCK_SIZE:
                break
    return True
