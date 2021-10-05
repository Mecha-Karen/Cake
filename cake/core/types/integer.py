from ..number import Number
from cake.abc import IntegerType
import typing


class Integer(Number):
    """
    A class representing a whole number, subclass of :class:`~cake.Number`

    Parameters
    ----------
    number: :class:`~cake.abc.IntegerType`
        Any object which matches the `IntegerType` protocol.
        Defaults to 0
    check_value_attr: :class:`bool`
        See `me </cake/api/index.html#cake.Number.value>`
    *args: :class:`~typing.Any`
        See `me </cake/api/index.html#cake.Number.value>`
    """

    def __init__(
        self, integer: IntegerType = 0,
        check_value_attr: bool = True,
        *args, **kwargs
    ):
        super().__init__(
            int(integer), check_value_attr,
            int, Integer, *args, **kwargs
        )

    @staticmethod
    def handler(res: IntegerType, chk_value: bool, _, __, *args, **kwargs):
        return Integer(
            integer=int(res),
            check_value_attr=chk_value,
            *args, **kwargs
        )

    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Integer({super().value})"
