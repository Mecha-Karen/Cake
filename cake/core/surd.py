from math import sqrt

from .number import Number
from cake import errors


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
