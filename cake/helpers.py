import typing
import cake

__all__ = ("convert_type", "compare_multiple", "compare_any")


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

    if hasattr(result, 'value'):
        return result

    if len(str(result).split(".")) > 1:
        return cake.Float(result, check_value_attr, *args, **kwargs)

    try:
        return cake.Complex(raw=str(result))
    except ValueError:
        pass

    try:
        ir = cake.Irrational(result, check_value_attr, *args, **kwargs)
    except ValueError:
        return result

    return ir


def compare_multiple(*args, type: typing.Type) -> bool:
    """
    Compare 2 objects side by side by providing a type

    Parameters
    ----------
    *args: :class:`~typing.Any`
        Arguments to compare
    type: :class:`~typing.Type`
        A type object to compare the args to
    """
    matching = None

    for arg in args:
        if matching is False:
            return False

        if isinstance(arg, type):
            matching = True
        else:
            matching = False

    return matching


def compare_any(*args, type: typing.Type) -> bool:
    """
    Same as compare multiple except returns ``True`` when any of the object match the type

    Parameters
    ----------
    *args: :class:`~typing.Any`
        Arguments to compare
    type: :class:`~typing.Type`
        A type object to compare the args to
    """
    return any(isinstance(i, type) for i in args)
