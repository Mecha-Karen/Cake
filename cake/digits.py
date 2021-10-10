import typing
import cake


class Zero(cake.Integer):
    """
    An object representing nothing, or simply the number ``0``.
    This object inherits :class:`~cake.Integer`, you can find more infomation on how it works there!

    Parameters
    ----------
    check_value_attr: :class:`~typing.Optional[bool]`
    """

    def __init__(self, check_value_attr: typing.Optional[bool] = False, *args, **kwargs):
        super().__init__(check_value_attr=check_value_attr, *args, **kwargs)

    def __repr__(self) -> str:
        return 'Zero()'
