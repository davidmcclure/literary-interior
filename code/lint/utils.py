

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


class safe_cached_property:

    def __init__(self, func):
        self.__doc__ = getattr(func, '__doc__')
        self.func = func

    def __get__(self, obj, cls):
        """Call function and swallow errors. Cache result as attribute.
        https://github.com/pydanny/cached-property
        """
        try:
            value = self.func(obj)
        except Exception as e:
            log.exception(e)
            value = None

        obj.__dict__[self.func.__name__] = value
        return value


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
