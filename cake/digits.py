import typing
import cake


class Zero(cake.Integer):
    """
    An object representing nothing, or simply the number ``0``.
    This object inherits :class:`~cake.Integer`, you can find more infomation on how it works there!

    Parameters
    ----------
    check_value_attr: :class:`~typing.Optional[bool]`
        When a user preforms an arithmetic action it will check the `other` argument for the `value` attribute
        If found, it replaces the argument with that value, else returns the original argument
    """

    def __init__(
        self, check_value_attr: typing.Optional[bool] = False, *args, **kwargs
    ):
        super().__init__(0, check_value_attr=check_value_attr, *args, **kwargs)

    def __repr__(self) -> str:
        return "Zero()"


class Imaginary(cake.Number):
    """
    An object representing an Imaginary number.

    Parameters
    ----------
    i: :class:`int`
        The value for i, for complexes it will be the value for ``b``.
    """
    def __init__(self, i: int = None) -> None:
        self.i = (i or 1) * 1j

        super().__init__(self.i, base_type=cake.Complex)

    def toComplex(self):
        """ Returns N.i as a :class:`~cake.Complex` """
        return cake.Complex(a=0, b=self.i.imag)

    def __repr__(self) -> str:
        return f"Imaginary({str(self.i)[:-1]})"


class Infinity(cake.Number):
    """
    A class representing infinity
    """
    VALUE = float('inf')

    def __init__(self, check_value_attr: typing.Optional[bool] = False, *args, **kwargs) -> None:
        super().__init__(Infinity.VALUE, check_value_attr, Infinity, *args, **kwargs)

    def __repr__(self) -> str:
        return f"Infinity()"


class NegativeInfinity(cake.Number):
    """
    A class representing negative infinity
    """
    VALUE = float('-inf')

    def __init__(self, check_value_attr: typing.Optional[bool] = False, *args, **kwargs) -> None:
        super().__init__(NegativeInfinity.VALUE, check_value_attr, NegativeInfinity, *args, **kwargs)

    def __repr__(self) -> str:
        return f"NegativeInfinity()"


class NaN(cake.Number):
    """ A class representing NaN """
    VALUE = float('nan')

    def __init__(self, check_value_attr: typing.Optional[bool] = False, *args, **kwargs) -> None:
        super().__init__(NaN.VALUE, check_value_attr, NegativeInfinity, *args, **kwargs)

    def __repr__(self) -> str:
        return "NaN()"
    
