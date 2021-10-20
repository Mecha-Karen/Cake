# Utilities for documenting
import typing
import importlib


def copyDocString(function: typing.Union[str, typing.Callable]) -> typing.Callable:
    if isinstance(function, str):
        *package, name = function.split('.')
        mod = importlib.import_module('.'.join(package), name)
        function = getattr(mod, name)

    def inner(func):
        func.__doc__ == function.__doc__

        return func
    return inner
