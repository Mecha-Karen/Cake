from .trig import *
from .elem import *

from .trig import __all__ as trigA
from .elem import __all__ as elem

from difflib import get_close_matches


__all__ = trigA + elem


def getClosestMatch(name: str) -> None:
    return get_close_matches(name, __all__)
