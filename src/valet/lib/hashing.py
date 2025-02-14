import hashlib


def file_hash(filepath, digest = 'sha1'):
    """
    :param pathlib.Path filepath:
    :param digest: Passed into hashlib.file_digest
    """
    with filepath.open('rb') as f:
        return hashlib.file_digest(f, digest)
