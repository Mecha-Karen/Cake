from ..number import Number
from cake.abc import FloatType


class Float(Number):
    """
    A class representing a real number, subclass of :class:`~cake.core.number.Number`

    Parameters
    ----------
    number: :class:`~cake.abc.FloatType`
        Any object which matches the `FloatType` protocol.
        Defaults to 0
    """

    def __init__(
        self, real: FloatType = 0, check_value_attr: bool = True, *args, **kwargs
    ):
        super().__init__(real, *args, **kwargs, check_value_attr=check_value_attr)

        # Change base typing
        self._type = float

    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Real({super().value.real})"


Real = Float
