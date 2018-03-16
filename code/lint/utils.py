

import re
import logging
import csv

from functools import wraps

from . import fs


def try_or_none(func):
    """Call function in a try block. On error, return None.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):

        log = logging.getLogger('lint')

        try:
            return func(*args, **kwargs)
        except Exception as e:
            log.exception(e)
            return None

    return wrapper


class cached_class_property:

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        """Call function and cache result as class property.
        https://github.com/pydanny/cached-property
        """
        value = self.func(cls)
        setattr(cls, self.func.__name__, value)
        return value


def read_csv(path):
    """Generate row dicts from CSV.
    """
    lines = fs.read(path).read().decode().splitlines()
    yield from csv.DictReader(lines)


def clean_text(text):
    """Clean a raw text string.
    """
    return re.sub('\s+', ' ', text.strip())
