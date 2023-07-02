import sys
import config.dep_def as dep_def
import tarfile
import zipfile


def extract(file, format, dest):
    if format == dep_def.TAR_GZ:
        with tarfile.open(file, 'r:gz') as tar:
            tar.extractall(dest)
    if format == dep_def.TAR_BZ2:
        with tarfile.open(file, 'r:bz2') as tar:
            tar.extractall(dest)
    if sys.version >= '3':
        if format == dep_def.TAR_XZ:
            with tarfile.open(file, 'r:xz') as tar:
                tar.extractall(dest)
    if format == dep_def.ZIP:
        with zipfile.ZipFile(file, 'r') as zip:
            zip.extractall(dest)
