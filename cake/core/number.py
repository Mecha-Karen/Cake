"""
***********************
cake.core.number.Number
***********************
The root class for pretty much any number, digit in this library.
"""

from math import ceil
from .unknown import Unknown
import typing


class Number(object):
    r"""
    Base class for creating digits, unknowns etc.

    If creating an unknown, its best to use the `Unknown` class instead of this
    . Mainly due to the handling of an unknown is implemented in this class

    An unknown should only be used when the value is not known, meaning it can be anything.
    Else implement the `Range` class.
    
    For Quaternion's, the :class:`~cake.Number.value` can be a :class:`tuple`, or the class itself.

    Parameters
    ----------
    value: :class:`~typing.Any`
        The value that the class holds, can be a letter, digit, float etc.
    check_value_attr: :class:`bool`
        When a user preforms an arithmetic action it will check the `other` argument for the `value` attribute
        If found, it replaces the argument with that value, else returns the original argument
    base_type: :class:`~typing.Callable[[typing.Any], typing.Any]`
        A function or class, which is used to convert the input value to, defaults to :class:`float`
    *args: :class:`~typing.Any`
        Additional arguments which you may supply when using arithmetic operators such as ``+``
    **kwargs: :class:`~typing.Any`
        Additional keyword arguments which you may supply when using arithmetic operators such as ``+``
    
    Returns
    -------
    A number class which can handle all python operators
    """

    def __init__(self, value: typing.Any,
        check_value_attr: bool = True, 
        base_type: typing.Callable[[..., ], typing.Any] = float,
        *args, **kwargs,
    ):
        self._value = base_type(value)
        self._type = base_type

        self.check_value_attr = check_value_attr

        self.args = args
        self.kwargs = kwargs

    # ##############
    #
    # Dunder methods
    #
    # ##############

    def __call__(self, other, check_value_attr: bool = True, *args, **kwargs):
        """

        """

        other = self._get_value(other, check_value_attr, *args, **kwargs)

        if isinstance(other, Unknown):
            other.multiply(self)

            return other

        result = self._value * other

        return super(Number, self).__new__(Number, result)

    def __abs__(self):
        if self._value < 0:
            new_val = self._value * -1
        else:
            new_val = self._value

        return super(Number, self).__new__(Number, new_val)

    def __add__(self, other):
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.add(self)

            return other

        result = self._value + other

        return super(Number, self).__new__(Number, result)

    def __sub__(self, other):
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.add(self)

            return other

        result = self._value - other

        return super(Number, self).__new__(Number, result)

    def __mul__(self, other):
        return self.__call__(other, 
            self.check_value_attr, *self.args,
            **self.kwargs
        )

    def __ceil__(self):

        return ceil(self._value)

    def __truediv__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.truediv(self)

            return other

        result = self._value / other

        return super(Number, self).__new__(Number, result)

    def __floordiv__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.floordiv(self)

            return other

        result = self._value // other

        return super(Number, self).__new__(Number, result)

    def __mod__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.mod(self)

            return other

        result = self._value % other

        return super(Number, self).__new__(Number, result)

    def __divmod__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.divmod(self)

            return other

        result = divmod(self._value, other)

        return super(Number, self).__new__(Number, result)

    def __pow__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.pow(self)

            return other

        result = self._value ** other

        return super(Number, self).__new__(Number, result)

    def __lshift__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.lshift(self)

            return other

        result = self._value << other

        return super(Number, self).__new__(Number, result)

    def __rshift__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.rshift(self)

            return other

        result = self._value >> other

        return super(Number, self).__new__(Number, result)

    def __and__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other._and(self)

            return other

        result = self._value & other

        return super(Number, self).__new__(Number, result)

    def __xor__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.xor(self)

            return other

        result = self._value ^ other

        return super(Number, self).__new__(Number, result)

    def __or__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other._or(self)

            return other

        result = self._value | other

        return super(Number, self).__new__(Number, result)

    # #########
    #
    # Comparing
    #
    # #########

    def __lt__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self._value < float(other)

    def __le__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self._value <= float(other)

    def __gt__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self._value > float(other)

    def __ge__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self._value >= float(other)

    def __eq__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self._value == float(other)

    def __ne__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self._value != float(other)

    # ################
    #  
    # Type Conversion
    #
    # #################

    def __bool__(self):
        return self._value != 0

    def __int__(self):
        return int(self._value)

    def __float__(self):
        return float(self._value)

    def __complex__(self):
        return complex(self._value)

    def __str__(self):
        return str(self._value)

    # ################
    #
    # Other Attributes
    #
    # ################

    def __repr__(self) -> str:
        return f'Number({self._value})'

    @property
    def value(self) -> typing.Any:
        """
        Returns the value supplied when initialising the class, if it has been converted to the provided type, then that value is returned instead.
        """
        return self._value

    @value.setter
    def set_value(self, value: typing.Any) -> None:
        conversionType = self._type

        self._value = conversionType(value)

    @value.deleter
    def remove_value(self) -> None:
        self._value = 0


    @property
    def type(self) -> typing.Callable[[..., ], typing.Any]:
        """
        Returns the value type which was set when intialising the class, this will always return the actual class which you was set.

        This value is over-ridable
        """

        return self._type

    @type.setter
    def set_type(self, newType: typing.Callable[[..., ], typing.Any]) -> None:
        try:
            self._value = newType(self._value)
        except Exception as e:
            if isinstance(e, TypeError) and not callable(newType):
                raise TypeError(f'{newType.__qualname__} is not callable') from e
            raise TypeError(f'"{self._value}" could not be converted to the new type ({newType.__qualname__})') from e
        self._type = newType


    # @property
    # def sqrt(self):
    #    from .surd import Surd
    #
    #    is_rational = sqrt(self)
    #    if int(is_rational) - is_rational != 0:
    #        return Surd(is_rational)
    #
    #    return super(Number, self).__new__(Number, is_rational)

    def _get_value(self, other, check_value_attr, *args, **kwargs):
        if hasattr(other, 'value') and check_value_attr is True and not isinstance(other, Unknown):
            if callable(other.value):
                other = int(other.value(*args, **kwargs))
            else:
                other = int(other.value)
        return other
