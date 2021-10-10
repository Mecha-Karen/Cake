from math import sqrt
import math
import typing

from .number import Number
from .types.float import Float

from cake.abc import IntegerType
from cake.helpers import convert_type

from functools import cache

def get_perfect_square(
    limit: int, *, 
    increment: typing.Optional[int] = 3,
    index: typing.Optional[int] = 0,
    accumulated_list: typing.Optional[typing.List[int]] = [1]
    ) -> typing.Union[tuple]:

    while (accumulated_list[-1] + increment) <= limit:
        accumulated_list.append(accumulated_list[index] + increment)
        index += 1 
        increment = (2 * index) + 3
    return accumulated_list


def _rationalise(n: int, **kwargs) -> typing.Union[tuple, int]:
    from cake import Imaginary

    if n < 0:
        return Imaginary(n, math.sqrt)

    if sqrt(n).is_integer():
        return sqrt(n) 

    ac_list = get_perfect_square(n / 2, **kwargs)

    factors = [square for square in ac_list if n % square == 0 and square > 1]
    if len(factors) == 0:
        return n

    a = int(sqrt(max(factors)))
    b = int(n / max(factors))

    return a, b


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
        Coefficient of the unsolved root
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

    def __init__(self, integer, n = 1, i = 1) -> None:
        if isinstance(n, str):
            if not n.startswith('(') and not n.endswith(')'):
                raise ValueError(f'Formatting of fraction powers must be in the form of `(x/y)`')
            n = n[1:-1]
            n = map(convert_type, n.split('/'))

        self.integer = integer
        self.n = n
        self.i = i

        super().__init__(self.integer, True, float, Surd, Surd)

    # Some utilities
    def rationalise(self, **kwargs):
        from cake import Imaginary

        res = _rationalise(self.value, **kwargs)

        if isinstance(res, Imaginary):
            return res
        
        if isinstance(res, int):
            return Float(int)
        co, ac = res

        return Surd(
            ac, self.n, co
        )

    @property
    def decimal(self):
        if self.co != 1:
            integer = self.integer * (self.co ** 2)
        else:
            integer = self.integer

        if isinstance(self.n, tuple):
            x, y = self.n

            return convert_type(((integer ** (1 / y)) ** x) ** self.i)
        
        return convert_type((integer ** (1 / self.n)) ** self.i)

    @property
    def simplify(self):
        return self.decimal

    @property
    def evaluate(self):
        return self.decimal

    def __repr__(self) -> str:
        if self.i and self.i != 1:
            co = str(self.i)
        else:
            co = ''

        if self.n and self.n != 1:
            n = f'** {self.n}'
        else:
            n = ''

        return f'{co}√{self.integer} {n}'
