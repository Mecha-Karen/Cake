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
        expr = cake.Expression(repr(self))
        data = {self.value: value, **kwargs}

        return expr.substitute(*args, **data)

    def _getTerms(self) -> list:
        return cake.Expression(repr(self)).terms

    # MULTIPLICATION / DIVISION

    def multiply(self, O, *, create_new: bool = True, swap: bool = False):
        """
        Multiply your unknown value

        Parameters
        ----------
        O: :class:`~typing.Any`
            The value to multiply the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``*=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        # *

        if isinstance(O, cake.Expression):
            expr = O.expression

            expr = f"{repr(self)} * ({expr})"

            return cake.Expression(expr, *O.args, **O.kwargs)

        if isinstance(O, Unknown):
            Oterms = O._getTerms()
        else:
            Oterms = getattr(O, 'terms', [O])

        terms = self._getTerms()

        res = cake.Zero()

        for term in terms:
            for Oterm in Oterms:
                if isinstance(term, Unknown):
                    if isinstance(Oterm, Unknown) and Oterm.value == self.value:
                        res += term ** Oterm
                    elif isinstance(Oterm, Unknown):
                        nterm = term.copy()
                        nterm.data['operators']['multi'] *= Oterm.data['operators']['multi']
                        res += nterm
                    else:
                        nterm = term.copy()
                        nterm.data['operators']['multi'] *= Oterm
                        res += nterm

                elif isinstance(Oterm, Unknown):
                    nterm = Oterm.copy()
                    nterm.data['operators']['multi'] *= term
                    res += nterm
                else:
                    res += term * Oterm
                    
        return res

    def truediv(self, O, *, create_new: bool = True, swap: bool = False):
        """
        Divide your unknown value

        Parameters
        ----------
        O: :class:`~typing.Any`
            The value to divide the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``/=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        # /

        if getattr(O, "value", O) == 0:
            raise ZeroDivisionError("division by zero")

        if isinstance(O, cake.Expression):
            expr = O.expression

            expr = f"{repr(self)} / ({expr})"

            return cake.Expression(expr, *O.args, **O.kwargs)

        elif isinstance(O, Unknown) and O.value == self.value:
            cur_power = self.data["raised"]

            OPower = O.data["raised"]

            if OPower == None:
                OPower = 1
            if cur_power == None:
                cur_power = 1

            # Special powers

            if isinstance(OPower, list):
                raise NotImplementedError(
                    f"listed fractional powers is not supported yet"
                )

            try:
                fractional = FRACTIONAL_POWER.match(OPower)
            except TypeError:
                fractional = None

            if fractional:
                raise NotImplementedError(
                    f"Fraction + Fraction actions are not yet supported"
                )

            if OPower != 1:
                if not create_new:
                    self.data["raised"] = cur_power - OPower
                    return self

                data = cp.deepcopy(self.data)
                data["raised"] = cur_power - OPower

                return Unknown(data)

        cur_res = self.data["operators"]["div"]

        if cur_res is None:
            cur_res = 0

        try:
            res = cur_res + O
        except Exception:
            res = O + cur_res

        if not create_new:
            self.data["operators"]["div"] = res
            self.data['Dswap'] = swap
            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["div"] = res
        copy['Dswap'] = swap

        return Unknown(value=self.value, **copy)

    # FLOOR DIVISION / MODULUS

    def floordiv(self, O, *, create_new: bool = True, swap: bool = False):
        """
        Divide your unknown value with no remainders

        Parameters
        ----------
        O: :class:`~typing.Any`
            The value to divide the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``//=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        # //

        if getattr(O, "value", O) == 0:
            raise ZeroDivisionError("integer division or modulo by zero")

        if isinstance(O, cake.Expression):
            expr = O.expression

            expr = f"{repr(self)} // ({expr})"

            return cake.Expression(expr, *O.args, **O.kwargs)

        cur_res = self.data["operators"]["fdiv"]

        if cur_res is None:
            cur_res = 0

        try:
            res = O + cur_res
        except Exception:
            res = cur_res + O

        if not create_new:
            self.data["operators"]["fdiv"] = res
            self.data['Fswap'] = swap
            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["fdiv"] = res
        copy['Fswap'] = swap

        return Unknown(value=self.value, **copy)

    def mod(self, O, *, create_new: bool = True, swap: bool = False):
        """
        Modulo your unknown value

        Parameters
        ----------
        O: :class:`~typing.Any`
            The value to mod the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``*=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """
        ## %

        if getattr(O, "value", O) == 0:
            raise ZeroDivisionError("integer division or modulo by zero")

        if isinstance(O, cake.Expression):
            expr = O.expression

            expr = f"{repr(self)} % ({expr})"

            return cake.Expression(expr, *O.args, **O.kwargs)

        cur_res = self.data["operators"]["mod"]

        if cur_res is None:
            cur_res = 0

        try:
            res = O + cur_res
        except Exception:
            res = cur_res + O

        if not create_new:
            self.data["operators"]["mod"] = res
            self.data['Mswap'] = swap
            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["mod"] = res
        copy["Mswap"] = swap

        return Unknown(value=self.value, **copy)

    # POWER

    def pow(self, O, *, create_new: bool = True, swap: bool = False):
        """
        raise your unknown value to a value

        Parameters
        ----------
        O: :class:`~typing.Any`
            The value to raise the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``**=`` will always return the same object

            .. note::

                This is a keyword-only argument!
        """

        if isinstance(O, list):
            O = cake.Fraction(*O)

        if isinstance(O, Unknown):

            if self.data['raised'] == 1 and O.data['raised'] == 1:
                raised = 2
            else:
                raised = self.data['raised'] * O.data['raised']

            if not create_new:
                self.data['raised'] = raised
                return
            x = self.copy()
            x.data['raised'] = raised
            return x

        if not create_new:
            self.data['raised'] *= O
            return

        x = self.copy()
        x.data['raised'] *= O

        return x

    # ADDITION / SUBTRACTION

    def add(self, O, *, create_new: bool = True, swap: bool = False, negate: bool = False):
        """
        Add your unknown value, The subtraction method piggy banks this method and simply negates your value before sending it through here.
        So ``Unknown.add(-10)`` is equal to ``Unknown.subtract(10)``

        Parameters
        ----------
        O: :class:`~typing.Any`
            The value to add the unknown by
        create_new: :class:`bool`
            Whether to create a new object or return the same object
            arithmetic operators like ``+=`` will always return the same object
        swap: :class:`bool`
            Inverse the op, so `N + O` becomes `O + N`
        negate: :class:`bool`
            Usually paired with ``swap``, so `O` becomes `-O`.

            When paired with, ``swap`` `N - O` becomes `O - N`  
        """
        # +

        if isinstance(O, cake.Expression):
            expr = O.expression

            expr = f"{repr(self)} + ({expr})"

            return cake.Expression(expr, *O.args, **O.kwargs)

        try:
            res = O + self.data["operators"]["add"]
        except Exception:
            res = self.data["operators"]["add"] + O

        if not create_new:
            self.data["operators"]["add"] = res
            self.data['Aswap'] = swap
            self.data['Aneg'] = negate

            return self

        copy = cp.deepcopy(self.data)
        copy["operators"]["add"] = res

        copy['Aswap'] = swap
        copy['Aneg'] = negate

        return Unknown(value=self.value, **copy)

    def subtract(self, O, *, create_new=True, swap: bool = False, negate: bool = False):
        """
        Refer to the ``add`` method for more info
        """
        return self.add(-O, create_new=create_new, swap=swap, negate=negate)

    # DUNDER METHODS

    def __str__(self):
        return repr(self)

    def __repr__(self) -> str:
        return _prettify_repr(self)

    # UNARY

    def __pos__(self) -> "Unknown":
        """ Returns N """
        return self.copy()

    def __neg__(self) -> "Unknown":
        """ Negates N, Same as doing N * -1 """
        return self * -1

    def __invert__(self) -> "Unknown":
        """ Inverts bits for the value of N when provided """
        import operator

        cp = self.copy()
        cp.data['functions'].append(operator.invert)

        return cp

    # Arithmetic

    def __mul__(self, O) -> "Unknown":
        return self.multiply(O)

    def __call__(self, O) -> "Unknown":
        return self.multiply(O)

    def __add__(self, O) -> "Unknown":
        return self.add(O)

    def __sub__(self, O, *, swap: bool = False) -> "Unknown":
        # Nifty shortcut
        return self.add(-O, swap=swap)

    def __truediv__(self, O):
        return self.truediv(O)

    def __floordiv__(self, O):
        return self.floordiv(O)

    def __mod__(self, O):
        return self.mod(O)

    def __pow__(self, O):
        return self.pow(O)

    # Rep dunders
    def __rmul__(self, O):
        return self * O

    def __radd__(self, O):
        return self + O

    def __rsub__(self, O):
        return self.add(O, swap=True, negate=True)

    def __rtruediv__(self, O):
        return self.truediv(O, swap=True)

    def __rfloordiv__(self, O):
        return self.floordiv(O, swap=True)

    def __rmod__(self, O):
        return self.mod(O, swap=True)

    def __rpow__(self, O):
        return self.pow(O, swap=True)

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

# Delayed to prevent cyclic import
from .repr import _prettify_repr
