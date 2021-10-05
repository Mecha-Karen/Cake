from cake.parsing.expression import Expression
from math import exp, factorial as fc
from cake.abc import PRETTY_PRINT_SYMBOLS, UNKNOWN_PRETTIFIER_SYMBOL
import typing

VALID_DATA_KEYS = {
    "raised": 1,
    "multiplied": 1,
    "op": None,
    "sqrt": False,
    "factorial": False,
}

class Unknown(object):

    """
    An object representing an unknown value

    Parameters
    ----------
    value: :class:`str`
        A letter which represents the unknown value
    **data: :class:`~typing.Optional[cake.core.unknown.VALID_DATA_KEYS]`
        Any additional data for the unknown, e.g. if its raised to a power
    """
    def __init__(self, value: str, **data):
        self.value = value
        self.data = {**VALID_DATA_KEYS, **data}

        for key in data.keys():
            if key not in VALID_DATA_KEYS:
                self.data.pop(key)

    def parse(self, dirty_string: str) -> "Unknown":
        raise NotImplementedError()

    def multiply(self, other):
        from ..parsing.expression import Expression

        if isinstance(other, Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} * ({expr})'

            return super(Expression, self).__new__(Expression, expr)

        self.multiplied = (self.multiplied * other)

        return self
        

    def add(self, other):
        raise NotImplementedError()

    def floordiv(self, other):
        raise NotImplementedError()

    def divmod(self, other):
        raise NotImplementedError()

    def mod(self, other):
        raise NotImplementedError

    def truediv(self, other):
        raise NotImplementedError()

    def pow(self, other):
        raise NotImplementedError()

    def lshift(self, other):
        raise NotImplementedError()

    def rshift(self, other):
        raise NotImplementedError()

    def _and(self, other):
        raise NotImplementedError() 

    def xor(self, other):
        raise NotImplementedError()

    def _or(self, other):
        raise NotImplementedError()

    def __getattr__(self, name: str) -> typing.Any:
        is_valid_attr = self.__dict__.get(name)

        if not is_valid_attr:
            try:
                return self.data[name]
            except KeyError:
                pass
        else:
            return is_valid_attr
        
        raise AttributeError(f'{self.__class__.__qualname__} has no attribute {name}')

    def __setattr__(self, name: str, value: typing.Any) -> None:
        try:
            attr = self.data[name]
            attr_type = type(VALID_DATA_KEYS[name])
        except KeyError as e:
            raise AttributeError(f'Cannot set attribute "{name}"') from e

        try:
            attr = attr_type(attr)
        except Exception as e:
            raise AttributeError(f'Failed to set attribute "{name}", "{value}" is of incorrect typing') from e
        self.data[name] = attr

    def __repr__(self, *, safe: bool = False) -> str:
        """
        For debugging and forming pretty-printed versions of an equation object

        Parameters
        ----------
        safe: :class:`bool`
            Removes any unknown characters and symbols and returns a parsable unknown
        """
        value = self.value
        raised = self.data['raised']

        if self.sqrt:
            if not safe:
                value = '√' + value
            else:
                value = f"sqrt({value})"

        if raised and str(raised) != '1':
            if not safe:
                squares = ''
                for sq in str(raised):
                    sym = PRETTY_PRINT_SYMBOLS['powers'].get(sq, UNKNOWN_PRETTIFIER_SYMBOL)
                    squares += sym

                value += squares

            else:
                value += f' ** {raised}'

        if self.factorial:
            value += '!'

        if not safe:
            return f'Unknown({value})'
        return f'({value})'
