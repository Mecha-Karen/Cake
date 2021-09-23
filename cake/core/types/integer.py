from cake import Number
from cake.abc import IntegerType

import typing


class Integer(Number):
    """
    A class representing a whole number, subclass of :class:`~cake.core.number.Number`

    Parameters
    ----------
    number: :class:`~cake.abc.IntegerType`
    """
    def __init__(
        self, integer: IntegerType,
        check_value_attr: bool = True,
        *args, **kwargs
    ):
        super().__init__(
            int(integer), check_value_attr,
            int, Integer, *args, **kwargs
        )

    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Integer({super().value})"
