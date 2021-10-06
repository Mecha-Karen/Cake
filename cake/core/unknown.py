import math
import re
from cake.abc import PRETTY_PRINT_SYMBOLS, UNKNOWN_PRETTIFIER_SYMBOL
import typing

VALID_DATA_KEYS = {
    "raised": 1,
    "multiplied": 1,
    "divided": 1,
    "op": 0,
    "sqrt": False,
    "factorial": False,
    "functions": []
}

FRACTIONAL_POWER = re.compile(r'\([0-9]+\/[0-9]+\)')

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

        if value.startswith('-'):
            self.negated = True

    def parse(self, dirty_string: str) -> "Unknown":
        raise NotImplementedError()

    def substitute(self, value, *args, **kwargs) -> typing.Any:
        from cake import Irrational, Integer, convert_type

        DATA = self.data
        NEW_VALUE = value

        for function in DATA['functions']:
            NEW_VALUE = function(NEW_VALUE, *args, **kwargs)
        
        POWER = DATA['raised']
        DIVISION = DATA['divided']
        MULTIPLICATION = DATA['multiplied']
        OP = DATA['op']

        if POWER:
            fractional = FRACTIONAL_POWER.match(str(POWER))

            if isinstance(POWER, list):
                indice, root = POWER
                FRACTIONAL = True
            elif fractional:
                group = fractional.group()[1:-1]
                indice, root = map(Irrational, group.split('/'))
                FRACTIONAL = True
            else:
                FRACTIONAL = False

            if FRACTIONAL:
                root = NEW_VALUE ** (Integer(1) / root)
                NEW_VALUE = root ** indice

            else:
                NEW_VALUE = NEW_VALUE ** POWER

        if DIVISION:
            NEW_VALUE /= DIVISION

        if MULTIPLICATION:
            NEW_VALUE *= MULTIPLICATION

        if OP:
            NEW_VALUE += OP

        return convert_type(NEW_VALUE)

    def multiply(self, other, *, create_new: bool = True):
        from ..parsing.expression import Expression

        if isinstance(other, Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} * ({expr})'

            return Expression(expr, *other.args, **other.kwargs)

        res = (other * self.data['multiplied'])
        # Allows `Number` classes to be used

        if not create_new:
            self.data['multiplied'] = res
            return self

        copy = self.data.copy()
        copy['multiplied'] = res

        return Unknown(value=self.value, **copy)

    def add(self, other, *, create_new: bool = True):
        from ..parsing.expression import Expression

        if isinstance(other, Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} + ({expr})'

            return Expression(expr, *other.args, **other.kwargs)

        res = (other + self.data['op'])

        if not create_new:
            self.data['op'] = res
            return self

        copy = self.data.copy()
        copy['op'] = res

        return Unknown(value=self.value, **copy)

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
        factorial = self.data['factorial']
        multip = self.data['multiplied']
        op = self.data['op']

        if multip and multip != 1:
            value = str(multip) + value

        if op and not isinstance(op, Unknown):
            if op < 0:
                value = str(op)[1:] + ' - ' + value
            else:
                value = str(op) + ' + ' + value
        elif op:                
            if getattr(op, 'negated', False):
                start = '-'
            else:
                start = ''

            value = f'{start}({op.__repr__(safe=safe)}) + ' + value

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

        if factorial:
            value += '!'

        if not safe:
            return f'Unknown({value})'
        return f'({value})'

    # Other dunder methods

    # Multiplication
    def __mul__(self, other) -> "Unknown":
        return self.multiply(other)

    def __call__(self, other) -> "Unknown":
        return self.multiply(other)

    # Addition/Subtraction
    def __add__(self, other) -> "Unknown":
        return self.add(other)

    def __sub__(self, other) -> "Unknown":
        # Nifty shortcut
        return self.add(-other)

    # Built in functions
    def __ceil__(self):
        data = self.data.copy()
        data['functions'].append(math.ceil)

        return Unknown(self.value, **data)

    def __ceil__(self):
        data = self.data.copy()
        data['functions'].append(abs)

        return Unknown(self.value, **data)

    # Properties
    
    @property
    def sub(self):
        # For the lazy people

        return self.substitute
