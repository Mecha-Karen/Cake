# Base mathmatical functions re-written to handle unknowns and other functions
from __future__ import annotations
import math
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

            res = self.handler.__self__.__class__(res)(*args, **kwargs)
        else:
            res = self.handler(other, *args, **kwargs)

        if hasattr(self, '_execAfter'):
            return self._execAfter(res)
        return res

    @property
    def hasNested(self) -> bool:
        """ Check if the function has another function in it """
        return self.functions != []

    def __repr__(self) -> str:
        value = getattr(self, '_value', '?')
        execA = getattr(self, '_execAfter', None)

        if execA:
            execA = execA.__qualname__
        
        return f'{self.name.title()}(functions={self.functions} handler={self.handler.__qualname__} execAfter={execA} is_multi={self.is_multi} value={value})'


class Function(FunctionBase, abc.ABC):
    """
    A simple wrapper function for the ``FunctionBase`` class

    .. seealso::

        `Example <https://github.com/Mecha-Karen/Cake/blob/main/examples/functions.py#L24>`_.
            An example of how to use the ``Function`` class
    """
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

    def execAfter(self, function) -> None:
        self._execAfter = function

    def __call__(self, *args, **kwargs) -> typing.Any:
        return super().evaluate(self._value, *args, **kwargs)


class MaskFunctionTemp(Function):
    """
    Create a ``Cake`` compat function using a pre-existing func

    Parameters
    ----------
    value: :class:`~typing.Any`
        A value for the function
    name: :class:`str`
        Name of the function
    function: :class:`~typing.Callable`
        A callable object, which acts as the main function.
        Whatever the ``value`` was set to is passed through.

        .. note::
            If ``type`` is specified to a value, it will be the value returned from that
    type: :class:`str`
        An optional string which is a function from the standard math library.
        This function will replace the ``value`` being passed into the ``function``.
    """
    def __init__(self, value, name, function, *, type: str = "radians"):
        super().__init__(value, name=name)
        
        self._type = type
        self._function = function

    def _raw_exec(self, other) -> typing.Any:
        if isinstance(other, cake.Unknown):
            unknown = other.copy()
            unknown.data['functions'].append(self.__class__)
            return unknown

        if hasattr(other, 'value'):
            other = other.value
        if hasattr(other, 'get_value'):
            other = other.get_value()

        otherConverter = getattr(math, self._type, None)
        if not otherConverter:
            val = other
        else:
            val = otherConverter(other)

        return cake.convert_type(self._function(val))
