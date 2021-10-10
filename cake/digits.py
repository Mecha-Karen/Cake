import typing
import cake


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

    Parameters
    ----------

    """
