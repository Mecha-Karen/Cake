import math
import re
from cake.abc import PRETTY_PRINT_SYMBOLS, UNKNOWN_PRETTIFIER_SYMBOL
import typing
import cake

VALID_DATA_KEYS = {
    "raised": 1,
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

            try:
                fractional = FRACTIONAL_POWER.match(otherPower)
            except TypeError:
                fractional = None

            if fractional:
                raise NotImplementedError(f'Fraction + Fraction actions are not yet supported')

            if otherPower != 1:
                res = (cur_power + otherPower)

            else:
                res = (cur_power + 1)

            if not create_new:
                self.data['raised'] = res
                return self

            copy = self.data.copy()
            copy['raised'] = res

            return Unknown(value=self.value, **copy)

        res = (other * self.data['operators']['multi'])
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

            try:
                fractional = FRACTIONAL_POWER.match(otherPower)
            except TypeError:
                fractional = None

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

            try:
                fractional = FRACTIONAL_POWER.match(otherPower)
            except TypeError:
                fractional = None

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

    def subtract(self, other, *, create_new = True):
        """
        Refer to the ``add`` method for more info
        """
        return self.add(-other, create_new=create_new)

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

    def __repr__(self) -> str:
        return _prettify_repr(self)

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

    @power.setter
    def set_power(self, new_Power: typing.Union[str, int, "Unknown", list]) -> None:
        if not isinstance(new_Power, (str, int, Unknown, list)):
            raise TypeError(f'Invalid power set')

        self.data['raised'] = new_Power

def _prettify_repr(unk: Unknown) -> str:
    """
    Returns a parsable repr of an unknown
    """
    value = unk.value
    raised = unk.data['raised']
    factorial = unk.data['factorial']
    multip = unk.data['operators']['multi']
    div = unk.data['operators']['div']
    add = unk.data['operators']['add']
    sqrt = unk.data['sqrt']
    factorial = unk.data['factorial']

    if factorial:
        value += '!'

    # BIDMAS pattern
    STRING = ""

    if raised and raised != 1:
        if not isinstance(raised, str):
            raised = repr(raised)

        STRING += f'{value} ** {raised}'

    if div:
        STRING += f' / {div}'

    if multip and multip != 1:
        STRING += f' * {multip}'

    if add:
        if add < 0:
            if isinstance(add, (cake.Number, float, int)):
                add = str(add)[1:]

            STRING += f' - {add}'
        else:
            STRING += f' + {add}'

    if sqrt:
        STRING = f'sqrt({STRING})'
    
    if factorial:
        STRING += '!'

    return STRING
