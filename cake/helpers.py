import typing
import cake
import copy as cd

from cake import abc

__all__ = ("convert_type", "compare_multiple", "compare_any", "copy")


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

    if result == abc.INF_VALUE:
        return cake.Infinity()
    if result == abc.NEG_INF_VALUE:
        return cake.NegativeInfinity()
    if result == abc.NAN_VALUE:
        return cake.NaN()

    if isinstance(result, cake.Number):
        return result

    if hasattr(result, 'value'):
        result = result.value
    if hasattr(result, 'get_value'):
        result = result.get_value()

    if isinstance(result, complex):
        if not result.imag:
            return cake.Float(result.real)
        return cake.Complex(result)

    if len(str(result).split(".")) > 1:
        return cake.Float(result, check_value_attr, *args, **kwargs)

    try:
        ir = cake.Irrational(result, check_value_attr, *args, **kwargs)
    except (ValueError, TypeError):
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


def copy(object):
    return cd.deepcopy(object)
