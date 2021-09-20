from math import ceil, sqrt
from .unknown import Unknown


class Real(object):
    def __init__(self, value: float = 0.0,
        check_value_attr: bool = True, 
        *args, **kwargs,
    ):
        self.__value = float(value)
        self.check_value_attr = check_value_attr

        self.args = args
        self.kwargs = kwargs

    # ##############
    #
    # Dunder methods
    #
    # ##############

    def __call__(self, other, check_value_attr: bool = True, *args, **kwargs):
        other = self._get_value(other, check_value_attr, *args, **kwargs)

        if isinstance(other, Unknown):
            other.multiply(self)

            return other

        result = self.__value * other

        return super(Real, self).__new__(Real, result)

    def __abs__(self):
        if self.__value < 0:
            return self.__value * -1
        return self.__value

    def __add__(self, other):
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.add(self)

            return other

        result = self.__value + other

        return super(Real, self).__new__(Real, result)

    def __sub__(self, other):
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.add(self)

            return other

        result = self.__value - other

        return super(Real, self).__new__(Real, result)

    def __mul__(self, other):
        return self.__call__(other, 
            self.check_value_attr, *self.args,
            **self.kwargs
        )

    def __ceil__(self):

        return ceil(self.__value)

    def __truediv__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.truediv(self)

            return other

        result = self.__value / other

        return super(Real, self).__new__(Real, result)

    def __floordiv__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.floordiv(self)

            return other

        result = self.__value // other

        return super(Real, self).__new__(Real, result)

    def __mod__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.mod(self)

            return other

        result = self.__value % other

        return super(Real, self).__new__(Real, result)

    def __divmod__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.divmod(self)

            return other

        result = divmod(self.__value, other)

        return super(Real, self).__new__(Real, result)

    def __pow__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.pow(self)

            return other

        result = self.__value ** other

        return super(Real, self).__new__(Real, result)

    def __lshift__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.lshift(self)

            return other

        result = self.__value << other

        return super(Real, self).__new__(Real, result)

    def __rshift__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.rshift(self)

            return other

        result = self.__value >> other

        return super(Real, self).__new__(Real, result)

    def __and__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other._and(self)

            return other

        result = self.__value & other

        return super(Real, self).__new__(Real, result)

    def __xor__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other.xor(self)

            return other

        result = self.__value ^ other

        return super(Real, self).__new__(Real, result)

    def __or__(self, value):
        other = self._get_value(value, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            other._or(self)

            return other

        result = self.__value | other

        return super(Real, self).__new__(Real, result)

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

        return self.__value < float(other)

    def __le__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self.__value <= float(other)

    def __gt__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self.__value > float(other)

    def __ge__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self.__value >= float(other)

    def __eq__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self.__value == float(other)

    def __ne__(self, other) -> bool:
        other = self._get_value(other, getattr(self, 'check_value_attr', True),
            *self.args, **self.kwargs
        )

        if isinstance(other, Unknown):
            raise TypeError('Cannot compare known with unknown')

        return self.__value != float(other)

    # ################
    #  
    # Type Conversion
    #
    # #################

    def __bool__(self):
        return self.__value != 0

    def __int__(self):
        return int(self.__value)

    def __float__(self):
        return float(self.__value)

    def __complex__(self):
        return complex(self.__value)

    def __str__(self):
        return str(self.__value)

    # ################
    #
    # Other Attributes
    #
    # ################

    def __repr__(self) -> str:
        return f'Real({self.__value})'

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def set_value(self, value) -> None:
        self.__value = float(value)

    @value.deleter
    def remove_value(self) -> None:
        self.__value = 0


    @property
    def sqrt(self):
        from .surd import Surd

        is_rational = sqrt(self)
        if int(is_rational) - is_rational != 0:
            return Surd(is_rational)

        return super(Real, self).__new__(Real, is_rational)

    def _get_value(self, other, check_value_attr, *args, **kwargs):
        if hasattr(other, 'value') and check_value_attr is True and not isinstance(other, Unknown):
            if callable(other.value):
                other = int(other.value(*args, **kwargs))
            else:
                other = int(other.value)
        return other
