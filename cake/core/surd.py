from math import sqrt

from .real import Real
from cake import errors


class Surd(Real):
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
            return Real(is_rational)

        return super(Surd, cls).__new__(cls, is_rational)

    def __init__(self, integer: int) -> None:
        self.integer = integer
        self.value = sqrt(integer)


    def _rationalise(self):
        raise NotImplementedError()

    
    def __add__(self, other) -> Real:
        if isinstance(other, Surd):
            ...
        
        return Real(self.value + other)