import hashlib
import config.dep_def as dep_def

ALGORITHM_MAP = {
    dep_def.MD5: hashlib.md5,
    dep_def.SHA1: hashlib.sha1,
    dep_def.SHA224: hashlib.sha224,
    dep_def.SHA256: hashlib.sha256,
    dep_def.SHA384: hashlib.sha384,
    dep_def.SHA512: hashlib.sha512,
}


def verify(file, algo, hash):
    digest = ALGORITHM_MAP[algo]()
    with open(file, 'rb') as f:
        BLOCK_SIZE = 1024 * 1024
        while True:
            buffer = f.read(BLOCK_SIZE)
            digest.update(buffer)
            if (len(buffer) < BLOCK_SIZE):
                break
    hash_calc = digest.hexdigest()
    return hash_calc.lower() == hash.lower()
