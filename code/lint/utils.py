

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
            # TODO: Log failure?
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
