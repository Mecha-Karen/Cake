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
from math import sqrt

from .number import Number
from . import errors


class Surd(Number):
    r"""
    An object representing an irrational number

    Parameters
    ----------
    integer : int

    """
    def __new__(cls, *args, **kwargs):
        try:
            integer = kwargs.get('integer', args[0])
        except IndexError as e:
            raise errors.MissingValue('No number was provided') from e

        is_rational = sqrt(integer)

        if int(is_rational) - is_rational == 0:
            return Number(is_rational)

        return super(Surd, cls).__new__(cls, is_rational)

    def __init__(self, integer: int) -> None:
        self.integer = integer
        self.value = sqrt(integer)


    def _rationalise(self):
        raise NotImplementedError()

    
    def __add__(self, other) -> Number:
        if isinstance(other, Surd):
            ...
        
        return Number(self.value + other)
