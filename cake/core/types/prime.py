from cake import Number
from cake.functions.prime import is_prime


class Prime(Number):
    """
    A class representing a prime number, this method MUST be called directly, other classes such as `Number` and `Integer` will not return this class.
    If input number is not prime, returns 

    Parameters
    ----------
    number: :class:`~cake.abc.IntegerType`
        Any object which matches the `IntegerType` protocol
    """

    def __init__(self):
        raise NotImplementedError()
