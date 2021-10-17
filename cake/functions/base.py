# Base matmatical functions re-written to handle unknowns and other functions
from __future__ import annotations
from math import exp
import typing
import cake
import abc


class FunctionBase(object):
    """
    Base class for functions
    """
    def __init__(self, *,
        name: str,
        handler: typing.Optional[typing.Callable] = ...,
        is_multi: typing.Optional[bool] = False,
        functions: typing.List[typing.Callable] = list()
    ) -> None:
        self.name = name
        self.is_multi = is_multi
        self.functions = functions
        self.handler = handler

    def evaluate(self, other, *args, **kwargs):
        if self.handler == ...:
            self.handler = getattr(self, "_raw_exec")
        
        if self.is_multi:
            res = cake.Zero()
            for func in self.functions:
                try:
                    res += func(*args, **kwargs)()
                except Exception as e:
                    try:
                        res += func(*args, **kwargs)
                    except Exception as f:
                        raise f from e

            return self.handler.__self__.__class__(res)(*args, **kwargs)

        return self.handler(other, *args, **kwargs)

    def __repr__(self) -> str:
        value = getattr(self, '_value', '?')
        return f'{self.name.title()}(functions={self.functions} handler={self.handler.__qualname__} is_multi={self.is_multi} value={value})'


class Function(FunctionBase, abc.ABC):
    def __init__(self, value, *, name: str) -> None:
        functions = list()

        if isinstance(value, FunctionBase):
            is_multi = True
            for function in value.functions:
                functions.append(function)
            functions.append(value)
        else:
            is_multi = False

        super().__init__(
            name=name,
            handler=self._raw_exec,
            is_multi=is_multi,
            functions=functions,
        )

        self._value = value

    @abc.abstractmethod
    def _raw_exec(self, other) -> typing.Any:
        ...

    def __call__(self, *args, **kwargs) -> typing.Any:
        return super().evaluate(self._value, *args, **kwargs)