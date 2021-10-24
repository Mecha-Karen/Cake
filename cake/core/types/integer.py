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
    """

    def __init__(
        self,
        integer: typing.Optional[bool] = 0,
        check_value_attr: typing.Optional[bool] = True,
        *args,
        **kwargs,
    ):
        super().__init__(int(integer), check_value_attr, int, Integer, *args, **kwargs)

    @staticmethod
    def handler(res: IntegerType):
        return Integer(integer=int(res))

    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Integer({super().value})"
