"""
***********************
cake.core.number.Number
***********************
The root class for pretty much any number, digit in this library.
"""

from math import ceil, floor, trunc
from ..unknown.unknown import Unknown
import typing

from .ops import evaluate
import cake


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
    base_type: :class:`~typing.Callable`
        A function or class, which is used to convert the input value to, defaults to :class:`float`

    Returns
    -------
    :class:`~cake.Number`
    """

    def __init__(
        self,
        value: typing.Any,
        check_value_attr: bool = True,
        base_type: typing.Callable  = float,
        *args,
        **kwargs,
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

    def __call__(self, O):
        """
        Implementation of chaining, Multiplies O

        Parameters
        ---------
        O: :class:`~cake.abc.IntegerType`
            A class which follows the ``cake.abc.IntegerType`` and has the ``__mul__`` dunder method.
        """

        return evaluate(self.value, O, return_class=cake.convert_type, func='mul')

    # UNARY OPERATORS

    def __abs__(self):
        """ Get the absolute value of the number """
        if self._value < 0:
            new_val = self._value * -1
        else:
            new_val = self._value

        return cake.convert_type(new_val)

    def __neg__(self):
        """ Negate the number, multiplies it by ``-1`` """
        return cake.convert_type(self._value * -1)

    def __pos__(self):
        """ Returns the number in its normal form """
        return cake.convert_type(self._value)

    def __invert__(self):
        """ Inverts all of N's bits """
        return cake.convert_type(~self._value)

    # MATH FUNCTIONS

    def __round__(self, n=None):
        """ Rounds N to n """
        return cake.convert_type(round(self._value, n))
    
    def __trunc__(self):
        """ Truncates N """
        return cake.convert_type(trunc(self._value))

    def __floor__(self):
        """ Returns the :class:`floor` value of N """
        return cake.convert_type(floor(self._value))

    def __ceil__(self):
        """ Returns the :class:`floor` value of N """
        result = ceil(self._value)

        return cake.convert_type(result)

    # ARITHMETIC OPERATORS

    def __add__(self, O):
        """ Add the number with O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='add')

    def __sub__(self, O):
        """ Subtract the number with O """
        return evaluate(self.value, -O, return_class=cake.convert_type, func='sub')

    def __mul__(self, O):
        """ Mutliply the number with O """
        return self.__call__(O)

    def __truediv__(self, O):
        """ Divide the number with O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='truediv')

    def __floordiv__(self, O):
        """ Floordiv the number with O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='floordiv')

    def __mod__(self, O):
        """ Modulus the number with O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='mod')

    def __divmod__(self, O):
        """ Returns the divmod of the number with O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='divmod')

    def __pow__(self, O):
        """ Raise the number to the power of O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='pow')

    def __lshift__(self, O):
        """ Binary left shit by O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='lshift')

    def __rshift__(self, O):
        """ Binary right shift by O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='rshift')

    def __and__(self, O):
        """ Binary and with O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='and_')

    def __xor__(self, O):
        """ Binary xor with O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='xor')

    def __or__(self, O):
        """ Binary or with O """
        return evaluate(self.value, O, return_class=cake.convert_type, func='or_')

    ## Replicate dunders
    ## __r... dunders are called by `x + Number`

    def __radd__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='add')

    def __rsub__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='sub')
    
    def __rmul__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='mul')

    def __rtruediv__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='truediv')

    def __rfloordiv__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='floordiv')
    
    def __rmod__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='mod')
    
    def __rdivmod__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='divmod')
    
    def __rpow__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='pow')

    def __rlshift__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='lshift')

    def __rrshift__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='rshift')

    def __rand__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='and_')

    def __rxor__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='xor')

    def __ror__(self, O):
        return evaluate(O, self.value, return_class=cake.convert_type, func='or_')

    # Replacate R dunders
    # __i... dunders are called by `x += Number`

    def __iadd__(self, O):
        return O + self

    def __isub__(self, O):
        return O - self

    def __imul__(self, O):
        return O * self

    def __itruediv__(self, O):
        return O / self

    def __ifloordiv__(self, O):
        return O // self

    def __imod__(self, O):
        return O % self
    
    def __ipow__(self, O):
        return O ** self

    def __ilshift__(self, O):
        return O << self

    def __irshift__(self, O):
        return O >> self

    def __iand__(self, O):
        return O & self

    def __ixor__(self, O):
        return O ^ self

    def __ior__(self, O):
        return O | self

    # #########
    #
    # Comparing
    #
    # #########

    def __lt__(self, O) -> bool:
        """ Check if N < O """

        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=cake.convert_type, func='lt')

    def __le__(self, O) -> bool:
        """ Check if N <= O """

        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=cake.convert_type, func='le')

    def __gt__(self, O) -> bool:
        """ Check if N > O """

        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=cake.convert_type, func='gt')

    def __ge__(self, O) -> bool:
        """ Check if N >= O """

        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=cake.convert_type, func='ge')

    def __eq__(self, O) -> bool:
        """ Check if N == O """
        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=cake.convert_type, func='eq')

    def __ne__(self, O) -> bool:
        """ Check if N != O """
        if isinstance(O, Unknown):
            raise TypeError("Cannot compare known with unknown")

        return evaluate(self.value, O, return_class=cake.convert_type, func='ne')

    # ################
    #
    # Type Conversion
    #
    # #################

    def __bool__(self):
        """ Returns if N != 0 """
        return self._value != 0

    def __int__(self):
        """ Returns N as an int """
        return int(self._value)

    def __float__(self):
        """ Returns N as a float """
        return float(self._value)

    def __complex__(self):
        """ Returns N as a complex """
        return complex(self._value)

    def __str__(self):
        """ Returns N as a string """
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

        This is overridable and deletable, if deleted value is set to ``cake.Zero``.
        """
        return self._value

    @value.setter
    def set_value(self, value: typing.Any) -> None:
        conversionType = self._type

        self._value = conversionType(value)

    @value.deleter
    def remove_value(self) -> None:
        self._value = cake.Zero()

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
