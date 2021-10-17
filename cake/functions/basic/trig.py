# Trigonmetry functions
from ..base import Function
import cake
import typing
import math

__all__ = ("Sin", "Cos", "Tan")


class Cos(Function):
    def __init__(self, value) -> None:
        super().__init__(value, name="sin")

    def _raw_exec(self, other) -> typing.Any:
        if isinstance(other, cake.Unknown):
            unknown = other.copy()
            unknown.data['functions'].append(self.__class__)
            return unknown

        if hasattr(other, 'value'):
            other = other.value
        if hasattr(other, 'get_value'):
            other = other.get_value()

        radians = math.radians(other)

        return cake.convert_type(math.sin(radians))



class Cos(Function):
    def __init__(self, value) -> None:
        super().__init__(value, name="cos")

    def _raw_exec(self, other) -> typing.Any:
        if isinstance(other, cake.Unknown):
            unknown = other.copy()
            unknown.data['functions'].append(self.__class__)
            return unknown

        if hasattr(other, 'value'):
            other = other.value
        if hasattr(other, 'get_value'):
            other = other.get_value()

        radians = math.radians(other)

        return cake.convert_type(math.cos(radians))


class Tan(Function):
    def __init__(self, value) -> None:
        super().__init__(value, name="tan")

    def _raw_exec(self, other) -> typing.Any:
        if isinstance(other, cake.Unknown):
            unknown = other.copy()
            unknown.data['functions'].append(self.__class__)
            return unknown

        if hasattr(other, 'value'):
            other = other.value
        if hasattr(other, 'get_value'):
            other = other.get_value()

        radians = math.radians(other)

        return cake.convert_type(math.tan(radians))
