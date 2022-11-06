import os, hash_algo, urllib, tarfile, zipfile

CACHE_DIR = '.srcdep'

class UrlDepUpdater(object):
    @staticmethod
    def update(args, dir, dep):
        if os.path.exists(dep.PATH):
            return
        cache_file = os.path.join(dir, CACHE_DIR, dep.PATH)
        if os.path.exists(cache_file):
            print('File %s exists, verifying...' % cache_file)
            if not verify(cache_file, dep.URL_HASH):
                print('File %s verified error, re-download' % cache_file)
                os.remove(cache_file)
        if not os.path.exists(cache_file):
            download(dep.URL, cache_file)
            print('File %s downloaded, verifying...' % cache_file)
            if not verify(cache_file, dep.URL_HASH):
                print('File %s verified error, stop' % cache_file)
                return False
        extract_dir = dep.PATH
        if dep.ROOT_DIR is not None:
            extract_dir = os.path.dirname(dep.PATH)
        if dep.URL_FORMAT == 'tar.gz':
            with tarfile.open(cache_file, 'r:gz') as tar:
                tar.extractall(extract_dir)
        if dep.URL_FORMAT == 'tar.bz2':
            with tarfile.open(cache_file, 'r:bz2') as tar:
                tar.extractall(extract_dir)
        if dep.URL_FORMAT == 'zip':
            with zipfile.open(cache_file, 'r') as zip:
                zip.extractall(extract_dir)
        if dep.ROOT_DIR is not None:
            os.rename(os.path.join(extract_dir, dep.ROOT_DIR), dep.PATH)

def verify(file, url_hashes):
    for url_hash in url_hashes:
        print('Verifying %s = %s...' % (url_hash.ALGORITHM, url_hash.HASH))
        if not hash_algo.verify(file, url_hash.ALGORITHM, url_hash.HASH):
            return False
    return True

def download(url, file):
    print('Downloading %s to %s ...' %(url, file))
    if not os.path.exists(os.path.dirname(file)):
        os.makedirs(os.path.dirname(file))
    remote = urllib.urlopen(url)
    with open(file, 'wb') as local:
        BLOCK_SIZE = 1024*1024
        while True:
            buffer = remote.read(BLOCK_SIZE)
            local.write(buffer)
            if len(buffer) < BLOCK_SIZE:
                break
