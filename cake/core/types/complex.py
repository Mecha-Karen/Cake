from math import radians
from ..number import Number
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
        self, a: typing.Optional[IntegerType] = 0, b: typing.Optional[IntegerType] = 0,
        raw: typing.Optional[str] = None,
        check_value_attr: typing.Optional[bool] = True,
        *args, **kwargs
    ):
        if raw:
            raw = str(raw)

            if raw[0] == '(' and raw[-1] == ')':
                raw = raw[1:-1]

            a, b = raw.split('+')
            if b.endswith(('i', 'j')):
                b = b[:-1]
            else:
                raise ValueError('Incorrect formatting for complex number, should be in the format of "a + bi"')
        
        if isinstance(a, complex) and not b:
            integer = a
        elif isinstance(a, complex) and isinstance(b, complex):
            # Sum both complexes
            integer = a + b
        else:
            integer = complex(float(a), float(b))

        super().__init__(
            integer, check_value_attr,
            complex, Complex, *args, **kwargs
        )

    @staticmethod
    def handler(res: complex, chk_value: bool, _, __, *args, **kwargs):
        return Complex(
            a = res.real,
            b = res.imag,
            check_value_attr=chk_value,
            *args, **kwargs
        )

    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Complex({super().value})"
