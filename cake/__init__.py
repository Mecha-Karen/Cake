r"""
Cake
----
An object orientated maths library

:copyright: (c) 2021-present Seniatical
:license: MIT, see LICENSE for more details.
"""

from math import *

from .utils import patterns
from .errors import *

from .equation import Equation
from .number import Number
from .surd import Surd

__file__ = __import__('os').path.abspath(__file__)
__doc__ = 'An object orientated maths library'
