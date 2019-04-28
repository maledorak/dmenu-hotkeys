from distutils.spawn import find_executable


def is_installed(app):
    if not find_executable(app):
        raise SystemError("\"{}\" is not installed in your system "
                          "or don't exists in PATH".format(app))
    return True


class _Singleton(type):
    """
    A metaclass that creates a Singleton base class when called.
    based on: https://stackoverflow.com/a/6798042
    works in Python 2 & 3

    Implementation:
    `class SomeClass(_Singleton('SingletonMeta', (object,), {})):`
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_Singleton, cls).__call__(
                *args, **kwargs)
        return cls._instances[cls]

    def _clean_singleton(cls):
        cls._instances = {}
