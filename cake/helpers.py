import typing
import cake

__all__ = ("convert_type",)


def convert_type(
    result: typing.Any, check_value_attr: bool = True, *args, **kwargs
) -> object:
    """
    Returns an object of the specified type, this is helpful for the built-in objects, such as ``Integer``

    Parameters
    ----------
    result: :class:`~typing.Any`
        The result/object to convert the type to
    """
    if not result:
        return cake.Zero()

    if len(str(result).split(".")) > 1:
        return cake.Float(result, check_value_attr, *args, **kwargs)

    try:
        return cake.Complex(raw=str(result))
    except ValueError:
        pass
    ir = cake.Irrational(result, check_value_attr, *args, **kwargs)

    return ir
