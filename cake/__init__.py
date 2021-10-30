from cake.core.number import Number
from math import *
from typing import NamedTuple, Literal

from .errors import *

# Core Types
from .core import *

from .parsing import Expression, Equation

from .matrices.matrix import Matrix
from .matrices.shorthand import *
from .fractions import *

# Functions
from .functions import *

# Graphs
from .graphs import *

# Files
from .errors import *
from .abc import *
from .helpers import *
from .sympy import *
from .digits import *

from . import errors, abc, helpers, sympy, digits

__file__ = __import__("os").path.abspath(__file__)
__doc__ = "An object orientated math library"
__version__ = "0.0.1a3"
__author__ = "Mecha Karen"


class VersionInfo(NamedTuple):
    major: int
    minor: int
    micro: int
    level: Literal["Alpha", "Beta", "Stable", "Final"]


version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=1, level="Pre-Alpha")
