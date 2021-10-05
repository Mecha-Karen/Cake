import typing

__all__ = (
    "convert_type"
)


def convert_type(result: typing.Any, check_value_attr: bool = True, *args, **kwargs) -> object:
    """
    Returns an object of the specified type, this is helpful for the built-in objects, such as ``Integer``

    Parameters
    ----------
    result: :class:`~typing.Any`
        The result/object to convert the type to
    """
    from .core import (Complex, Float, Irrational)

    if len(str(result).split('.')) > 1:
        return Float(result, check_value_attr, *args, **kwargs)
    
    try:
        return Complex(raw=str(result))
    except ValueError:
        pass
    ir = Irrational(result, check_value_attr, *args, **kwargs)

    return ir
