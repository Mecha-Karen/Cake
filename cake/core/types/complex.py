from ..number import Number
from cake.abc import IntegerType
import typing
import cake


class Complex(Number):
    """
    A class representing a complex number, subclass of :class:`~cake.Number`

    A complex is number which can be expressed in the form of ``a + bi``, were a and b are integers.
    Learn more `here <https://en.wikipedia.org/wiki/Complex_number>`_

    .. note::

        If parameters ``a`` and ``b`` are complexes, the value of the complex will be ``a + b``.

    Parameters
    ----------
    a: :class:`cake.abc.IntegerType`
        Any object which matches the `IntegerType` protocol.
        Defaults to 0
    b: :class:`cake.abc.IntegerType`
        Any object which matches the `IntegerType` protocol.
        Defaults to 0
    raw: :class:`str`
        A string which represents the complex in the form ``(a + bi)``
    """

    def __init__(
        self,
        a: typing.Optional[IntegerType] = 0,
        b: typing.Optional[IntegerType] = 0,
        raw: typing.Optional[str] = None,
        check_value_attr: typing.Optional[bool] = True,
        *args,
        **kwargs,
    ):
        if raw:
            raw = str(raw)

            if raw[0] == "(" and raw[-1] == ")":
                raw = raw[1:-1]

            a, b = raw.split("+")
            if b.endswith(("i", "j")):
                b = b[:-1]
            else:
                raise ValueError(
                    'Incorrect formatting for complex number, should be in the format of "a + bi"'
                )

        if cake.helpers.compare_multiple(a, b, type=(complex, Complex)):
            # Sum both complexes
            integer = a + b
        else:
            if not isinstance(a, (complex, Complex)) and a:
                a = float(a)
            if not isinstance(b, (complex, Complex)) and b:
                b = float(b)

            # Fool-proof for NoneType
            integer = complex((a or 0), (b or 0))

        super().__init__(integer, check_value_attr, complex, *args, **kwargs)

    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Complex({super().value})"
