"""
MIT License

Copyright (c) 2021 Mecha Karen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from math import *
from typing import NamedTuple, Literal

from .errors import *

from .equation import Equation
from .number import Number
from .surd import Surd

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
