

from cached_property import cached_property


def try_or_none(f):
    """Wrap a method call in a try block. If an error is raised, return None.
    """
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return None
    return wrapper


def safe_cached_property(f):
    return cached_property(try_or_none(f))
