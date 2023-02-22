import functools
from functools import update_wrapper


def property_cache(f):

    name = "_cache_" + f.__name__

    @property
    @functools.wraps(f)
    def decorator(self):
        if not hasattr(self, name):
            setattr(self, name, f(self))
        return getattr(self, name)

    return decorator


class lazy_property:
    r"""
    Used as a decorator for lazy loading of class attributes. This uses a
    non-data descriptor that calls the wrapped method to compute the property on
    first call; thereafter replacing the wrapped method into an instance
    attribute.
    """

    def __init__(self, fget):
        self.fget = fget
        update_wrapper(self, fget)
        self._clear = False

    def __get__(self, instance, obj_type=None):
        if instance is None:
            return self
        value = self.fget(instance)
        setattr(instance, self.fget.__name__, value)
        return value


class lazy_property_clearable:
    r"""
    Used as a decorator for lazy loading of class attributes. This uses a
    non-data descriptor that calls the wrapped method to compute the property on
    first call; thereafter replacing the wrapped method into an instance
    attribute.
    """

    def __init__(self, fget):
        self.cache = {}
        self.fget = fget
        update_wrapper(self, fget)

    def __get__(self, instance, obj_type=None):
        if instance is None:
            return self
        if instance not in self.cache:
            self.cache[instance] = self.fget(instance)
        return self.cache[instance]

    def clear(self):
        self.cache.clear()
