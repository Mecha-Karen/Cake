import math
import re
from cake.abc import PRETTY_PRINT_SYMBOLS, UNKNOWN_PRETTIFIER_SYMBOL
import typing
import cake

VALID_DATA_KEYS = {
    "raised": 1,
    "multiplied": 1,
    "operators": {
        "div": None,
        "multi": 1,
        "fdiv": None,
        "mod": None,
        "add": 0
    },
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
        """
        Converts a stringed value into a proper object

        .. code-block:: py

            >>> from cake import Unknown
            >>> x = Unknown.parse("x ** 2")
            >>> x
            Unknown(x²)

        Parameters
        ----------
        dirty_string: :class:`str`
            The string to evaluate
        """
        raise NotImplementedError()

    def substitute(self, value, *args, **kwargs) -> typing.Any:
        """
        Replaces your unknown value with the provided value, and evaluates it

        Parameters
        ----------
        value: :class:`~typing.Any`
            A value to replace your unknown with

        .. note::

            Args and kwargs may be supplied, they will used for any functions used on the unknown
            The same set of args and kwargs will be used for every function
        """
        from cake import Irrational, Integer, convert_type

        DATA = self.data
        NEW_VALUE = value

        for function in DATA['functions']:
            NEW_VALUE = function(NEW_VALUE, *args, **kwargs)
        
        POWER = DATA['raised']
        DIVISION = DATA['operators']['div']
        MULTIPLICATION = DATA['operators']['multi']
        OP = DATA['operators']['add']

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

    # MULTIPLICATION / DIVISION

    def multiply(self, other, *, create_new: bool = True):
        """
        Multiply your unknown value

        Parameters
        ----------
        other: :class:`~typing.Any`
            The value to multiply the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``*=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        # *

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} * ({expr})'

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        elif isinstance(other, Unknown) and other.value == self.value:
            cur_power = self.data['raised']

            otherPower = other.data['raised']

            if isinstance(otherPower, list):
                raise NotImplementedError(f'listed fractional powers is not supported yet')

            fractional = FRACTIONAL_POWER.match(otherPower)

            if fractional:
                raise NotImplementedError(f'Fraction + Fraction actions are not yet supported')

            if otherPower != 1:
                if not create_new:
                    self.data['raised'] = (cur_power + otherPower)
                    return self

                data = self.data.copy()
                data['raised'] = (cur_power + otherPower)

                return Unknown(data)

        res = (other * self.data['multiplied'])
        # Allows `Number` classes to be used

        if not create_new:
            self.data['operators']['multi'] = res
            return self

        copy = self.data.copy()
        copy['operators']['multi'] = res

        return Unknown(value=self.value, **copy)

    def truediv(self, other, *, create_new: bool = True):
        """
        Divide your unknown value

        Parameters
        ----------
        other: :class:`~typing.Any`
            The value to divide the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``/=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        # /

        if getattr(other, 'value', other) == 0:
            raise ZeroDivisionError('division by zero')

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} / ({expr})'

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        elif isinstance(other, Unknown) and other.value == self.value:
            cur_power = self.data['raised']

            otherPower = other.data['raised']

            # Special powers

            if isinstance(otherPower, list):
                raise NotImplementedError(f'listed fractional powers is not supported yet')

            fractional = FRACTIONAL_POWER.match(otherPower)

            if fractional:
                raise NotImplementedError(f'Fraction + Fraction actions are not yet supported')

            if otherPower != 1:
                if not create_new:
                    self.data['raised'] = (cur_power - otherPower)
                    return self

                data = self.data.copy()
                data['raised'] = (cur_power - otherPower)

                return Unknown(data)

        cur_res = self.data['operators']['div']

        if cur_res is None:
            cur_res = 0

        res = other + cur_res

        if not create_new:
            self.data['operators']['div'] = res
            return self

        copy = self.data.copy()
        copy['operators']['div'] = res

        return Unknown(value=self.value, **copy)


    # FLOOR DIVISION / MODULUS

    def floordiv(self, other, *, create_new: bool = True):
        """
        Divide your unknown value with no remainders

        Parameters
        ----------
        other: :class:`~typing.Any`
            The value to divide the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``//=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        # //

        if getattr(other, 'value', other) == 0:
            raise ZeroDivisionError('integer division or modulo by zero')

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} // ({expr})'

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        cur_res = self.data['operators']['fdiv']

        if cur_res is None:
            cur_res = 0

        res = other + cur_res

        if not create_new:
            self.data['operators']['fdiv'] = res
            return self

        copy = self.data.copy()
        copy['operators']['fdiv'] = res

        return Unknown(value=self.value, **copy)

    def mod(self, other, *, create_new: bool = True):
        """
        Modulo your unknown value

        Parameters
        ----------
        other: :class:`~typing.Any`
            The value to mod the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``*=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        ## %

        if getattr(other, 'value', other) == 0:
            raise ZeroDivisionError('integer division or modulo by zero')

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} % ({expr})'

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        cur_res = self.data['operators']['mod']

        if cur_res is None:
            cur_res = 0

        res = other + cur_res

        if not create_new:
            self.data['operators']['mod'] = res
            return self

        copy = self.data.copy()
        copy['operators']['mod'] = res

        return Unknown(value=self.value, **copy)

    # POWER

    def pow(self, other, *, create_new: bool = True):
        """
        raise your unknown value to a value

        Parameters
        ----------
        other: :class:`~typing.Any`
            The value to raise the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``**=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        cur_power = self.data['raised']

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} ** ({expr})'

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        elif isinstance(other, Unknown) and other.value == self.value:
            otherPower = other.data['raised']

            if isinstance(otherPower, list):
                raise NotImplementedError(f'listed fractional powers is not supported yet')

            fractional = FRACTIONAL_POWER.match(otherPower)

            if fractional:
                raise NotImplementedError(f'Fraction + Fraction actions are not yet supported')

            cur_power = cur_power * otherPower
        else:
            cur_power = other * cur_power

        if not create_new:
            self.data['raised'] = cur_power
            return self

        data = self.data.copy()
        data['raised'] = cur_power

        return Unknown(self.value, **data)


    # ADDITION / SUBTRACTION

    def add(self, other, *, create_new: bool = True):
        """
        Add your unknown value, The subtraction method piggy banks this method and simply negates your value before sending it through here.
        So ``Unknown.add(-10)`` is equal to ``Unknown.subtract(10)``

        Parameters
        ----------
        other: :class:`~typing.Any`
            The value to add the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``+=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        # +

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f'{self.__repr__(safe=True)} + ({expr})'

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        res = (other + self.data['operators']['add'])

        if not create_new:
            self.data['operators']['add'] = res
            return self

        copy = self.data.copy()
        copy['operators']['add'] = res

        return Unknown(value=self.value, **copy)

    def subtraction(self, other, *, create_new):
        """
        Refer to the ``add`` method for more info
        """
        return self.add(-other, create_new=create_new)

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

    # DUNDER METHODS

    def __str__(self):
        return self.value

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
        multip = self.data['operators']['multi']
        div = self.data['operators']['div']
        op = self.data['operators']['add']

        if raised and str(raised) != '1':
            if not safe:
                squares = ''
                for sq in str(raised):
                    sym = PRETTY_PRINT_SYMBOLS['powers'].get(sq, UNKNOWN_PRETTIFIER_SYMBOL)
                    squares += sym

                value += squares

            else:
                value += f' ** {raised}'

        if div and div != 1:
            value += f' / {div}'

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

            value = f'{start}({super(op).__repr__()}) + ' + value

        if self.sqrt:
            if not safe:
                value = '√' + value
            else:
                value = f"sqrt({value})"

        if factorial:
            value += '!'

        if not safe:
            return f'Unknown({value})'
        return f'({value})'

    # Arithmetic

    def __mul__(self, other) -> "Unknown":
        return self.multiply(other)

    def __call__(self, other) -> "Unknown":
        return self.multiply(other)

    def __add__(self, other) -> "Unknown":
        return self.add(other)

    def __sub__(self, other) -> "Unknown":
        # Nifty shortcut
        return self.add(-other)

    def __truediv__(self, other):
        return self.truediv(other)

    def __floordiv__(self, other):
        return self.floordiv(other)

    def __mod__(self, other):
        return self.mod(other)

    def __pow__(self, other):
        return self.pow(other)

    # Built in functions
    def __ceil__(self):
        data = self.data.copy()
        data['functions'].append(math.ceil)

        return Unknown(self.value, **data)

    def __abs__(self):
        data = self.data.copy()
        data['functions'].append(abs)

        return Unknown(self.value, **data)

    # Properties

    @property
    def sub(self):
        # For the lazy people

        return self.substitute

    @property
    def power(self):
        return self.data['raised']

    @power.setter()
    def set_power(self, new_Power: typing.Union[str, int, "Unknown", list]) -> None:
        if not isinstance(new_Power, (str, int, Unknown, list)):
            raise TypeError(f'Invalid power set')

        self.data['raised'] = new_Power
