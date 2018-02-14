

import os
import re
import scandir
import io

from urllib.parse import urlparse

from .conn import s3


# TODO: Break into separate package, test.


def is_s3(path):
    """Is a path an S3 object path?
    """
    return bool(re.match('s3[a|n]?:\/\/', path))


def parse_s3_url(url):
    """Parse the bucket name and path from a s3:// URL.

    Args:
        url (str)

    Returns: bucket name, prefix
    """
    parsed = urlparse(url)

    return parsed.netloc, parsed.path.lstrip('/')


def scan(path, pattern=None):
    """Generate files that match a pattern.

    Args:
        path (str)
        pattern (str)
    """
    return (
        _scan_s3(path, pattern) if is_s3(path) else
        _scan_local(path, pattern)
    )


def _scan_local(path, pattern=None):
    """Scan local FS paths.
    """
    for root, dirs, files in scandir.walk(path, followlinks=True):
        for name in files:

            # Match the pattern.
            if not pattern or re.search(pattern, name):
                yield os.path.join(root, name)


def _scan_s3(path, pattern=None):
    """Scan S3 paths.
    """
    name, prefix = parse_s3_url(path)

    bucket = s3.Bucket(name)

    for obj in bucket.objects.filter(Prefix=prefix):

        # Match the pattern.
        if not pattern or re.search(pattern, obj.key):
            yield os.path.join('s3://', bucket.name, obj.key)


def read(path):
    """Read a file to BytesIO.

    Args:
        path (str)
    """
    return (
        _read_s3(path) if is_s3(path) else
        _read_local(path)
    )


def _read_local(path):
    """Read a local file.
    """
    with open(path, 'rb') as fh:
        return io.BytesIO(fh.read())


def _read_s3(path):
    """Read an S3 path.
    """
    bucket, key = parse_s3_url(path)

    obj = s3.Object(bucket, key)

    return io.BytesIO(obj.get()['Body'].read())
