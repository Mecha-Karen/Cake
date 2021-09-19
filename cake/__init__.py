from math import *
from typing import NamedTuple, Literal

from .errors import *

from .core import (
    Equation, Real, Surd, Unknown, Operator
)

from . import errors, abc

__file__ = __import__('os').path.abspath(__file__)
__doc__ = 'An object orientated maths library'
__version__ = "0.0.1a"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    level: Literal['Pre-Alpha', 'Alpha', 'Beta', 'Stable', 'Final']

version_info: VersionInfo = VersionInfo(
    major=0, minor=0, micro=1,
    level='Pre-Alpha'
) 
