from ..number import Number
from cake.abc import FloatType


class Float(Number):
    """
    A class representing a whole number, subclass of :class:`~cake.core.number.Number`

    Parameters
    ----------
    number: :class:`~cake.abc.FloatType`
        Any object which matches the `FloatType` protocol.
        Defaults to 0
    """

    def __init__(
        self, real: FloatType = 0, check_value_attr: bool = True, *args, **kwargs
    ):
        super().__init__(
            float(real), check_value_attr, float, FloatType, *args, **kwargs
        )

    @staticmethod
    def handler(res: FloatType):
        return Float(real=float(res))

    def __repr__(self) -> str:
        """
        Return the integer set when initialising the class
        """

        return f"Real({super().value})"


Real = Float
