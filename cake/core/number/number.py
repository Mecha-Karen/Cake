"""
***********************
cake.core.number.Number
***********************
The root class for pretty much any number, digit in this library.
"""

from functools import wraps
from math import ceil
from ..unknown import Unknown
import typing

from .ops import evaluate


class Number(object):
    r"""
    Base class for creating digits, unknowns etc.

    If creating an unknown, its best to use the `Unknown` class instead of this
    . Mainly due to the handling of an unknown is implemented in this class

    An unknown should only be used when the value is not known, meaning it can be anything.
    Else implement the `Range` class.

    For Quaternion's, the :class:`~cake.Number.value` can be a :class:`tuple`, or the class itself.

    .. _Parameters:

    Parameters
    ----------
    value: :class:`~typing.Any`
        The value that the class holds, can be a letter, digit, float etc.
    check_value_attr: :class:`bool`
        When a user preforms an arithmetic action it will check the `other` argument for the `value` attribute
        If found, it replaces the argument with that value, else returns the original argument
    base_type: :class:`~typing.Callable[[..., ], typing.Any]`
        A function or class, which is used to convert the input value to, defaults to :class:`float`
    return_me: :class:`typing.Callable[[..., ], typing.Any]`
        A function or class which is returned when an arithmetic operator is used on the class.
        This is different from `base_type` as this returns the specified class as opposed to just converting the input to specific type.
    return_handler: :class:`typing.Callable[[..., ], typing.Any]`
        skips the default return class and calls this method with the following arguments, in the same order.

        .. code-block:: text

            Result
            Check Value Attribute
            Type
            Current Return Class
            args
            kwargs


    *args: :class:`~typing.Any`
        Additional arguments which you may supply when using arithmetic operators such as ``+``
    **kwargs: :class:`~typing.Any`
        Additional keyword arguments which you may supply when using arithmetic operators such as ``+``

    Returns
    -------
    A number class which can handle all python operators
    """

    def __init__(
        self,
        value: typing.Any,
        check_value_attr: bool = True,
        base_type: typing.Callable  = float,
        return_me: typing.Callable = ...,
        return_handler: typing.Callable = None,
        *args,
        **kwargs,
    ):
        self._value = base_type(value)
        self._type = base_type

        self.check_value_attr = check_value_attr

        self.args = args
        self.kwargs = kwargs

        if return_me == ...:
            self.return_class = Number
        else:
            if hasattr(return_me, "handler"):
                if callable(return_me.handler):
                    self.return_class = return_me.handler
                else:
                    raise TypeError("handler must be a callable object")
            else:
                self.return_class = return_me

        if return_handler:
            # Lazy method of keeping short and consise handlers
            self.return_class = return_handler

    # ##############
    #
    # Dunder methods
    #
    # ##############

    def __call__(self, O):
        """
        Implementation of chaining, Action formed is multiplication

        Parameters
        ---------
        O: :class:`~cake.abc.IntegerType`
            A class which follows the ``cake.abc.IntegerType`` and has the ``__mul__`` dunder method.
        """

        return evaluate(self.value, O, return_class=self.return_class, func='mul')

    def __abs__(self):
        if self._value < 0:
            new_val = self._value * -1
        else:
            new_val = self._value

        return self.return_class(new_val)

    def __add__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='add')

    def __sub__(self, O):
        return evaluate(self.value, -O, return_class=self.return_class, func='add')

    def __neg__(self):
        return self.return_class(self.value * -1)

    def __mul__(self, other):
        return self.__call__(other)

    def __ceil__(self):
        result = ceil(self._value)

        return self.return_class(result)

    def __truediv__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='truediv')

    def __floordiv__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='floordiv')

    def __mod__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='mod')

    def __divmod__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='divmod')

    def __pow__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='pow')

    def __lshift__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='lshift')

    def __rshift__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='rshift')

    def __and__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='and_')

    def __xor__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='xor')

    def __or__(self, O):
        return evaluate(self.value, O, return_class=self.return_class, func='or_')

    # #########
    #
    # Comparing
    #
    # #########

    def __lt__(self, O) -> bool:

        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=self.return_class, func='lt')

    def __le__(self, O) -> bool:
        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=self.return_class, func='le')

    def __gt__(self, O) -> bool:
        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=self.return_class, func='gt')

    def __ge__(self, O) -> bool:
        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=self.return_class, func='ge')

    def __eq__(self, O) -> bool:
        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=self.return_class, func='eq')

    def __ne__(self, O) -> bool:
        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=self.return_class, func='ne')

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
        return f"Number({self._value})"

    @property
    def value(self) -> typing.Any:
        """
        Returns the value supplied when initialising the class, if it has been converted to the provided type, then that value is returned instead.

        This is overridable and deletable, if deleted value is set to 0.
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
    def type(
        self,
    ) -> typing.Callable:
        """
        Returns the value type which was set when intialising the class, this will always return the actual class which you was set.

        This value is overridable
        """

        return self._type

    @type.setter
    def set_type(
        self,
        newType: typing.Callable,
    ) -> None:
        try:
            self._value = newType(self._value)
        except Exception as e:
            if isinstance(e, TypeError) and not callable(newType):
                raise TypeError(f"{newType.__qualname__} is not callable") from e
            raise TypeError(
                f'"{self._value}" could not be converted to the new type ({newType.__qualname__})'
            ) from e
        self._type = newType

    def _get_value(self, other, check_value_attr, *args, **kwargs):
        if (
            hasattr(other, "value")
            and check_value_attr is True
            and not isinstance(other, Unknown)
        ):
            if callable(other.value):
                other = int(other.value(*args, **kwargs))
            else:
                other = int(other.value)
        return other
