import re
import string
import typing

from cake import abc

from cake import (
    Complex, Integer, Irrational, Prime, Real,

    Operator, Symbol
)

ASCII_CHARS = string.ascii_letters

################
#
# Regex patterns
#
################

FIND_UNKNOWNS = re.compile(
    "[a-zA-Z]+",
    re.IGNORECASE
)

LARGE_UNKNOWNS = re.compile(
    "[0-9][a-zA-Z]+",
    re.IGNORECASE
)

BLACKLISTED = list(abc.KEYWORDS.keys()) + list(abc.CONSTANTS.keys())


# Main Object

class Equation(object):
    """
    Create simple mathmatical equations and statements and solve by providing values.
    If you supply an equation with multiple lines, it splits them and returns a list of equations instead of a single equation object

    Example
    -------
    
    .. code-block:: py

        >>> from cake import Equation
        >>> circle, line = Equation('(x ** 2) + (y ** 2)\n2x + y')

    Parameters
    ----------
    equation: :class:`str`
        The statement used when processing your statement
    *default_args: :class:`~typing.Any`:
        Default set of arguments used when substituting the equation, IF they are not supplied during substitution.
        If you supply some, it skips the provided ones and uses the ones that havent been provided.

        Example
        -------
        
        .. code-block:: py

            >>> from cake import Equation
            >>> y = Equation("2x + 3", 1)
            >>> y._sub()
            [Integer(2), Operator(+), Integer(3)]
    **default_kwargs: :class:`~typing.Mapping[str, typing.Any]`
        A set of keyword arguments use when substituting the equation, IF they have not been supplied during substitution.
        Compared to ``default_args``, this allows you to choose which arguments to supply.

        **These will overwrite any values set in ``*args``!**

        Example
        -------

        .. code-block:: py

            >>> from cake import Equation
            >>> eq = Equation("x ** 2 + y ** 2")
            >>> eq._sub(y=10)
            [Unknown(x), Operator(+), Integer(100)]

    
    """
    def __new__(cls, equation: typing.Union[str, list], *default_args, **default_kwargs):
        multiple = equation.split('\n') if type(equation) == str else equation
        if len(multiple) > 1:
            eqs = list()

            for eq in multiple:
                eqs.append(Equation(eq, *default_args, **default_kwargs))
            return eqs

        return super(Equation, cls).__new__(Equation, *default_args, **default_kwargs)

    def __init__(self, equation: str, *default_args, **default_kwargs) -> None:
        default_args = list(default_args)

        self.__equation = equation
        self.args = default_args
        self.kwargs = default_kwargs

        self.__mappings = self._sort_values(*default_args, **default_kwargs)

    def _sort_values(self, *args, **kwargs) -> dict:
        unknowns = FIND_UNKNOWNS.findall(self.__equation)
        for value in unknowns.copy():
            # Copy stops the change size during iteration error

            if value in BLACKLISTED:
                unknowns.remove(value)


        as_dict = {i: [] for i in unknowns}
        keys = list(as_dict.keys())

        current_key = keys[0]
        current_index = 0

        for arg in args:
            current_key = keys[current_index]

            as_dict[current_key].append(arg)

            if (current_index + 1) > len(keys):
                current_index = 0
            else:
                current_index += 1

        for key, value in kwargs.items():
            if key in as_dict:
                recurances = sum(1 for i in unknowns if i == key)
                as_dict[key] = [value for i in range(recurances)]

        return as_dict

    def _sub(self, *args, **kwargs):
        self.update_variables(*args, **kwargs)

        unknown_mapping = self.__mappings
        presence = list()

        large_unknowns = LARGE_UNKNOWNS.findall(self.__equation)
        index = 0

        for lu in large_unknowns:
            num_end = 0
            while lu[num_end].isdigit():
                num_end += 1
            by_many = lu[:num_end]
            unknown = lu[num_end:]

            value = unknown_mapping[unknown]
            print(value)

        return presence

    def substitute(self, *args, **kwargs):
        raise NotImplementedError()

    def solve(self, *args, **kwargs):
        raise NotImplementedError()

    def wrap_all(self, operator: str, ending: str, *eq_args, **eq_kwargs) -> None:
        op = Operator(operator)

        eq = f'({self.__equation})'
        eq += f' {op.value} {ending}'

        self.__equation = eq

        self.update_variables(*eq_args, **eq_kwargs)

    def update_variables(self, *args, **kwargs) -> None:
        default_args = self.args + list(args)
        default_kwargs = {**self.kwargs, **kwargs}

        self.args = default_args
        self.kwargs = default_kwargs

        self.__mappings = self._sort_values(*default_args, **default_kwargs)

    @property
    def mapping(self):
        """ Returns a copy of the variable mappings for unknowns """
        return self.__mappings.copy()

    @property
    def equation(self):
        """ Returns a copy of the equation used when initialsing the class """
        return self.__equation

    def __repr__(self) -> str:
        """
        Returns the equation set when initialising the class
        """

        return self.equation

## Tests
eq = Equation('-b (+|-) sqrt ((b ** 2) - 4(a)(c))')
eq.wrap_all('divide', "2(a)")

print(eq._sub(b=10))
