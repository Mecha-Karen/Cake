# Trigonometric functions
from ..base import Function
import cake
import typing
import math

__all__ = ("Sin", "Cos", "Tan")


class Sin(Function):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, name="sin")

        self.type = type

    def _raw_exec(self, other) -> typing.Any:
        if isinstance(other, cake.Unknown):
            unknown = other.copy()
            unknown.data['functions'].append(self.__class__)
            return unknown

        if hasattr(other, 'value'):
            other = other.value
        if hasattr(other, 'get_value'):
            other = other.get_value()

        otherConverter = getattr(math, self.type, None)
        if not otherConverter:
            val = other
        else:
            val = otherConverter(other)

        return cake.convert_type(math.sin(val))



class Cos(Function):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, name="cos")

        self.type = type

    def _raw_exec(self, other) -> typing.Any:
        if isinstance(other, cake.Unknown):
            unknown = other.copy()
            unknown.data['functions'].append(self.__class__)
            return unknown

        if hasattr(other, 'value'):
            other = other.value
        if hasattr(other, 'get_value'):
            other = other.get_value()

        otherConverter = getattr(math, self.type, None)
        if not otherConverter:
            val = other
        else:
            val = otherConverter(other)

        return cake.convert_type(math.cos(val))


class Tan(Function):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, name="tan")

        self.type = type

    def _raw_exec(self, other) -> typing.Any:
        if isinstance(other, cake.Unknown):
            unknown = other.copy()
            unknown.data['functions'].append(self.__class__)
            return unknown

        if hasattr(other, 'value'):
            other = other.value
        if hasattr(other, 'get_value'):
            other = other.get_value()

        otherConverter = getattr(math, self.type, None)
        if not otherConverter:
            val = other
        else:
            val = otherConverter(other)

        return cake.convert_type(math.tan(val))
