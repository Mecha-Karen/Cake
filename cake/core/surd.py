from math import sqrt
import typing

from .number import Number
from .types.float import Float

from cake.abc import IntegerType
from cake.helpers import convert_type


class Surd(Number):
    r"""
    An object representing an irrational number, in the form of a surd.

    Parameters
    ----------
    integer: `~cake.abc.IntegerType` 
        The irrational integer
    n: `~cake.abc.IntegerType`
        the nth term of the root, e.g ``3`` is cube-root. Doing ``'(2/3)'`` will cube root it an then raise it to the power of 2
    i: :`~cake.abc.IntegerType`:
        the integer on the left hand side of the surd, more commonly respresented as ``i``.
        For example ``2√2`` is equal to ``2 * √2``
    """
    def __new__(cls, 
            integer: IntegerType,
            n: IntegerType = 1,
            i: IntegerType = 1,
        ) -> typing.Union["Surd", Float]:

        is_rational = sqrt(integer)

        if int(is_rational) - is_rational == 0:
            return Float(is_rational)

        return super(Surd, cls).__new__(Surd)

    def __init__(self, integer, n, i) -> None:
        if isinstance(n, str):
            if not n.startswith('(') and not n.endswith(')'):
                raise ValueError(f'Formatting of fraction powers must be in the form of `(x/y)`')
            n = n[1:-1]
            n = map(convert_type, n)

        self.integer = integer
        self.n = n
        self.i = i
        self.value = sqrt(integer)

    # Some utilities

    @property
    def decimal(self):
        if isinstance(self.n, tuple):
            x, y = self.n

            return (self.integer ** (1 / y)) ** x

    @property
    def simplify(self):
        return self.decimal

    @property
    def evaluate(self):
        return self.decimal
