from .float import Float
import typing


class Integer(Float):
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
        integer: typing.Optional[int] = 0,
        check_value_attr: typing.Optional[bool] = True,
        *args,
        **kwargs,
    ):
        super().__init__(int(integer), check_value_attr, *args, **kwargs)


    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Integer({int(super().value.real)})"
