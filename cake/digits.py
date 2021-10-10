from types import prepare_class
from cake.core.markers import ALLOWED
import typing
import cake


def forceImaginary(n: int):
    ...


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

    def __init__(self, check_value_attr: typing.Optional[bool] = False, *args, **kwargs):
        super().__init__(check_value_attr=check_value_attr, *args, **kwargs)

    def __repr__(self) -> str:
        return 'Zero'


class Imaginary(cake.Number):
    """
    An object representing an Imaginary number, You will find this object appearing when your trying to sqrt a negative and so on.
    When adding imaginaries, the value will become a complex!

    Parameters
    ----------
    value: :class:`~typing.Any`
        The value of the imaginary number
    cause: :class:`~typing.Callable`
        The function which lead to the imaginary integer, if making your own up.
        Simply use the ``forceImaginary`` function to represent it or ``None``
    letter: :class:`~typing.Optional[str]`
        A letter from either ``i``, ``j`` to represent the imaginary
    """
    ALLOWED_LETTERS = ['i', 'j']

    def __init__(self, value: typing.Any, cause: typing.Callable,
        letter: typing.Optional[str] = 'i',
        check_value_attr: typing.Optional[bool] = True,
        repr: typing.Optional[str] = '{self.callable.__qualname__}({self.value}){self.letter}',

        *args, **kwargs
    ):
        if letter.lower() not in Imaginary.ALLOWED_LETTERS:
            raise ValueError(f'Letter ({letter}) provided was not in: {", ".join(Imaginary.ALLOWED_LETTERS)}')

        self.value = value
        self.letter = letter

        if not cause:
            cause = forceImaginary

        self.cause = cause

        self.repr = repr

        super().__init__(
            value, check_value_attr, complex,
            cake.Complex, *args, **kwargs
        )

    def __repr__(self) -> str:
        return self.repr.format(self=self)
