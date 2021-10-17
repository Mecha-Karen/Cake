# Trigonmetry functions
from ..base import FunctionBase, Function
import cake
import typing
import math

__all__ = ("Sin", "Cos", "Tan")


class Sin(FunctionBase):
    def __init__(self, *, 
        name: str, 
        handler: typing.Optional[typing.Callable] = ..., 
        is_multi: typing.Optional[bool] = False, 
        raw: typing.Optional[typing.Callable] = None
    ) -> None:
        super().__init__(name, handler=self._raw_exec, is_multi=is_multi, raw=raw)

    def _raw_exec(self, other) -> typing.Any:
        if isinstance(other, cake.Unknown):
            other.data['functions'].append(self)
            return other

        if hasattr(other, 'value'):
            other = other.value
        if hasattr(other, 'get_value'):
            other = other.get_value()

        radians = math.radians(other)

        return cake.convert_type(math.sin(radians))

    def __call__(self, other, *args, **kwargs) -> typing.Any:
        return super().evaluate(other, *args, **kwargs)


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
