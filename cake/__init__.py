from math import *
from typing import NamedTuple, Literal

from .errors import *

# Core Types
from .core.number import Number
from .core.surd import Surd
from .core.unknown import Unknown

# Markers
from .core.markers import (
    Marker, Symbol, Operator, PlusOrMinus, Function
)

# Built in types
from .core.types import (
    Complex, Integer, Irrational, Prime, Real, Float
)

# Algebra
from .core.equation import Equation
from .core.expression import Expression

# Functions
from .functions.prime import (
    is_prime, factor_tree
)

# Files
from . import (
    errors, abc, helpers
)

__file__ = __import__('os').path.abspath(__file__)
__doc__ = 'An object orientated math library'
__version__ = "0.0.1a2"
__author__ = "Mecha Karen"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    level: Literal['Alpha', 'Beta', 'Stable', 'Final']

version_info: VersionInfo = VersionInfo(
    major=0, minor=0, micro=1,
    level='Pre-Alpha'
) 
