from cake import Number
from cake.abc import IntegerType
import typing


class Complex(Number):
    """
    A class representing a complex number, subclass of :class:`~cake.core.number.Number`

    A complex is number which can be expressed in the form of ``a + bi``, were a and b are integers.
    Learn more `here <https://en.wikipedia.org/wiki/Complex_number>`_

    Parameters
    ----------
    a: :class:`~cake.abc.IntegerType`
        Any object which matches the `IntegerType` protocol. Fills the 
        Defaults to 0
    check_value_attr: :class:`bool`
        See `me </cake/api/index.html#cake.Number.value>`
    *args: :class:`~typing.Any`
        See `me </cake/api/index.html#cake.Number.value>`
    """

    def __init__(
        self, a: IntegerType = 0, b: IntegerType = 0,
        raw: str = None,
        check_value_attr: bool = True,
        *args, **kwargs
    ):
        if raw:
            a, b = raw.split('+')
            if b.endswith(('i', 'j')):
                b = b[:-1]
            else:
                raise TypeError('Incorrect formatting for complex number, should be in the format of "a + bi"')
        
        integer = complex(float(a), float(b))

        super().__init__(
            integer, check_value_attr,
            complex, Complex, *args, **kwargs
        )

    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Complex({super().value})"
