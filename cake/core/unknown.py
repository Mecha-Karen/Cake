import math
import re
import typing
import cake
import copy as cp

__all__ = ("Unknown", "_prettify_repr")

FRACTIONAL_POWER = re.compile(r"\([0-9]+\/[0-9]+\)")


class Unknown(object):

    VALID_DATA_KEYS = {
        "raised": 1,
        "operators": {"div": None, "multi": 1, "fdiv": None, "mod": None, "add": 0},
        "sqrt": False,
        "factorial": False,
        "functions": [],
    }

    """
    An object representing an unknown value

    Parameters
    ----------
    value: :class:`str`
        A letter which represents the unknown value
    **data: :class:`~typing.Optional[cake.core.unknown.Unknown.VALID_DATA_KEYS]`
        Any additional data for the unknown, e.g. if its raised to a power
    """

    def __init__(self, value: str, **data):
        self.value = value

        self.data = cp.deepcopy(Unknown.VALID_DATA_KEYS)
        self.data.update(data)

        if value.startswith("-"):
            self.negated = True

    def copy(self) -> "Unknown":
        return Unknown(self.value, **cp.deepcopy(self.data))

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

        for function in DATA["functions"]:
            NEW_VALUE = function(NEW_VALUE, *args, **kwargs)
            if isinstance(NEW_VALUE, cake.Function):
                NEW_VALUE = NEW_VALUE()

        POWER = DATA["raised"]
        DIVISION = DATA["operators"]["div"]
        MULTIPLICATION = DATA["operators"]["multi"]
        OP = DATA["operators"]["add"]

        if POWER:
            fractional = FRACTIONAL_POWER.match(str(POWER))

            if isinstance(POWER, list):
                indice, root = POWER
                FRACTIONAL = True
            elif fractional:
                group = fractional.group()[1:-1]
                indice, root = map(Irrational, group.split("/"))
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

            expr = f"{self.__repr__(safe=True)} * ({expr})"

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        elif isinstance(other, Unknown) and other.value == self.value:

            cur_power = self.data["raised"]

            otherPower = other.data["raised"]

            if isinstance(otherPower, list):
                raise NotImplementedError(
                    f"listed fractional powers is not supported yet"
                )

            try:
                fractional = FRACTIONAL_POWER.match(otherPower)
            except TypeError:
                fractional = None

            if fractional:
                raise NotImplementedError(
                    f"Fraction + Fraction actions are not yet supported"
                )

            if otherPower != 1:
                res = cur_power + otherPower

            else:
                res = cur_power + 1

            if not create_new:
                self.data["raised"] = res
                return self

            copy = cp.deepcopy(self.data)
            copy["raised"] = res

            return Unknown(value=self.value, **copy)

        try:
            res = other * self.data["operators"]["multi"]
        except Exception:
            res = self.data["operators"]["multi"] * other

        # Allows `Number` classes to be used

        if not create_new:
            self.data["operators"]["multi"] = res
            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["multi"] = res

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

        if getattr(other, "value", other) == 0:
            raise ZeroDivisionError("division by zero")

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f"{self.__repr__(safe=True)} / ({expr})"

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        elif isinstance(other, Unknown) and other.value == self.value:
            cur_power = self.data["raised"]

            otherPower = other.data["raised"]

            # Special powers

            if isinstance(otherPower, list):
                raise NotImplementedError(
                    f"listed fractional powers is not supported yet"
                )

            try:
                fractional = FRACTIONAL_POWER.match(otherPower)
            except TypeError:
                fractional = None

            if fractional:
                raise NotImplementedError(
                    f"Fraction + Fraction actions are not yet supported"
                )

            if otherPower != 1:
                if not create_new:
                    self.data["raised"] = cur_power - otherPower
                    return self

                data = cp.deepcopy(self.data)
                data["raised"] = cur_power - otherPower

                return Unknown(data)

        cur_res = self.data["operators"]["div"]

        if cur_res is None:
            cur_res = 0

        try:
            res = cur_res + other
        except Exception:
            res = other + cur_res

        if not create_new:
            self.data["operators"]["div"] = res
            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["div"] = res

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

        if getattr(other, "value", other) == 0:
            raise ZeroDivisionError("integer division or modulo by zero")

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f"{self.__repr__(safe=True)} // ({expr})"

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        cur_res = self.data["operators"]["fdiv"]

        if cur_res is None:
            cur_res = 0

        try:
            res = other + cur_res
        except Exception:
            res = cur_res + other

        if not create_new:
            self.data["operators"]["fdiv"] = res
            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["fdiv"] = res

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

        if getattr(other, "value", other) == 0:
            raise ZeroDivisionError("integer division or modulo by zero")

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f"{self.__repr__(safe=True)} % ({expr})"

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        cur_res = self.data["operators"]["mod"]

        if cur_res is None:
            cur_res = 0

        try:
            res = other + cur_res
        except Exception:
            res = cur_res + other

        if not create_new:
            self.data["operators"]["mod"] = res
            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["mod"] = res

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
        cur_power = self.data["raised"]

        if isinstance(other, cake.parsing.Expression):
            expr = other.expression

            expr = f"{self.__repr__(safe=True)} ** ({expr})"

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        elif isinstance(other, Unknown) and other.value == self.value:
            otherPower = other.data["raised"]

            if isinstance(otherPower, list):
                raise NotImplementedError(
                    f"listed fractional powers is not supported yet"
                )

            try:
                fractional = FRACTIONAL_POWER.match(otherPower)
            except TypeError:
                fractional = None

            if fractional:
                raise NotImplementedError(
                    f"Fraction + Fraction actions are not yet supported"
                )

            cur_power = cur_power * otherPower
        else:
            try:
                cur_power = other + cur_power
            except Exception:
                cur_power = cur_power + other

        if not create_new:
            self.data["raised"] = cur_power
            return self

        data = cp.deepcopy(self.data)
        data["raised"] = cur_power

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

            expr = f"{self.__repr__(safe=True)} + ({expr})"

            return cake.parsing.Expression(expr, *other.args, **other.kwargs)

        try:
            res = other + self.data["operators"]["add"]
        except Exception:
            res = self.data["operators"]["add"] + other

        if not create_new:
            self.data["operators"]["add"] = res
            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["add"] = res

        return Unknown(value=self.value, **copy)

    def subtract(self, other, *, create_new=True):
        """
        Refer to the ``add`` method for more info
        """
        return self.add(-other, create_new=create_new)

    # DUNDER METHODS

    def __str__(self):
        return repr(self)

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
        data = cp.deepcopy(self.data)
        data["functions"].append(math.ceil)

        return Unknown(self.value, **data)

    def __abs__(self):
        data = cp.deepcopy(self.data)
        data["functions"].append(abs)

        return Unknown(self.value, **data)

    # Properties

    @property
    def sub(self):
        # For the lazy people

        return self.substitute

    @property
    def power(self):
        return self.data["raised"]

    @power.setter
    def _set_power(self, new_Power: typing.Union[str, int, "Unknown", list]) -> None:
        if not isinstance(new_Power, (str, int, Unknown, list)):
            raise TypeError(f"Invalid power set")

        self.data["raised"] = new_Power

    @property
    def sqrt(self) -> bool:
        return self.data["sqrt"]

    @sqrt.setter
    def _set_sqrt(self, new_val: bool) -> None:
        self.data["sqrt"] = bool(new_val)

    @property
    def factorial(self) -> bool:
        return self.data["factorial"]

    @factorial.setter
    def _set_factorial(self, new_val: bool) -> None:
        self.data["factorial"] = bool(new_val)


def _prettify_repr(unk: Unknown) -> str:
    """
    Returns a parsable version of an unknown
    """
    value = unk.value
    raised = unk.data["raised"]
    factorial = unk.data["factorial"]
    multip = unk.data["operators"]["multi"]
    div = unk.data["operators"]["div"]
    add = unk.data["operators"]["add"]
    sqrt = unk.data["sqrt"]
    factorial = unk.data["factorial"]

    STRING = value

    if factorial:
        value += "!"

    if raised and raised != 1:
        if isinstance(raised, Unknown):
            raised = f"({str(raised)})"
        else:
            raised = str(raised)
        STRING += f" ** {raised}"

    if div:
        if isinstance(div, Unknown):
            div = f"({str(div)})"
        else:
            div = str(div)
        STRING += f" / {div}"

    if multip and multip != 1:
        if isinstance(multip, Unknown):
            div = f"({str(div)})"
        else:
            div = str(div)
        STRING += f" * {div}"

    if add:
        passed = False

        try:
            negated = add < 0
            passed = True
        except Exception:
            pass

        if not passed:
            try:
                negated = getattr(add, "value", 0) < 0
            except TypeError:
                negated = getattr(add, "negated", False)

        if isinstance(add, Unknown):
            val = f"({str(add)})"
        else:
            val = str(add)

        if negated:
            STRING += f" - {val}"
        else:
            STRING += f" + {val}"

    if sqrt:
        STRING = f"sqrt({STRING})"

    return STRING
