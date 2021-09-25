from math import *
from typing import NamedTuple, Literal

from .errors import *

# Core Types
from .core.equation import Equation
from .core.number import Number
from .core.surd import Surd
from .core.unknown import Unknown

# Markers
from .core.operator import Operator
from .core.symbol import Symbol

# Built in types
from .core.types import (
    Complex, Integer, Irrational, Prime, Real, Float
)

from . import (
    errors, abc, helpers
)

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
