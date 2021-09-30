from math import factorial
from cake.core.markers import ALLOWED
from cake.core.number import Number
import re
import typing
import string

from cake import abc, errors

from cake import (
    Complex, Integer, Irrational, Prime, Float, Unknown,

    Operator, Symbol, PlusOrMinus, Function
)
from cake.helpers import convert_type

ASCII_CHARS = string.ascii_lowercase
# Use lowercases so `X` is equal to `x`
BLACKLISTED = list(abc.KEYWORDS.keys()) + list(abc.CONSTANTS.keys())
# Keywords that cant be assigned to an unknown
VALID_SYMBOLS = {
    "!", "(", ")"
}
# Used for parsing functions
BREAK_ON_LAST = True
# Iterates one last time including the last letter before breaking

################
#
# Regex patterns
#
################

FIND_UNKNOWNS = re.compile(
    "[a-zA-Z]+",
    re.IGNORECASE
)

INVALID_OPS = re.compile(
    "[a-zA-Z]+[0-9]+", re.IGNORECASE
)

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
            [Symbol('('), Integer(1), ..., Operator(+), Integer(3)]
    **default_kwargs: :class:`~typing.Mapping[str, typing.Any]`
        A set of keyword arguments use when substituting the equation, IF they have not been supplied during substitution.
        Compared to ``default_args``, this allows you to choose which arguments to supply.

        Example
        -------

        .. code-block:: py

            >>> from cake import Equation
            >>> eq = Equation("x ** 2 + y ** 2")
            >>> eq._sub(y=10)
            [Unknown(x), ..., Operator(+), Integer(10), ...]

    
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

        self.__equation = equation.lower()
        self.args = default_args
        self.kwargs = default_kwargs

        self.__mappings = self._sort_values(*default_args, **default_kwargs)

    def _sort_values(self, *args, **kwargs) -> dict:
        unknowns = FIND_UNKNOWNS.findall(self.__equation)
        for value in unknowns.copy():
            # Copy stops the change size during iteration error

            if value in BLACKLISTED:
                unknowns.remove(value)


        as_dict = {i: None for i in unknowns}
        keys = list(as_dict.keys())

        if not keys:
            return {}

        current_key = keys[0]
        current_index = 0

        for arg in args:
            if (current_index + 1) > len(keys):
                break

            as_dict[current_key] = arg
            current_index += 1

        for key, value in kwargs.items():
            if key in as_dict:
                as_dict[key] = value

        as_dict = {k: v for k, v in as_dict.items() if v != None}

        return as_dict

    def _sub(self, update_mappings: bool = False, *args, **kwargs):
        """
        Simple tokenization, returns a list of tokens. This is usually only important to parsing.
        An example of this can be found in the ``substitution`` method.

        Parameters
        ----------
        update_mappings: :class:`bool`
            Update the inner unknown mappings with any new args or kwargs
        *args, **kwargs: :class:`~typing.Any`
            Overwrites or adds to pre-existing inner mappings for unknown values
        """

        if update_mappings:
            self.update_variables(*args, **kwargs)
            unknown_mapping = self.__mappings
        else:
            unknown_mapping = self.update_variables(False, *args, **kwargs)

        invalid = INVALID_OPS.findall(self.equation)
        if invalid:
            found_first = invalid[0]
            index = 0

            while True:
                if index == len(found_first):
                    break

                if found_first[index].isdigit():
                    break
                index += 1

            possible_correct = found_first[:index]
            possible_correct += ' '
            possible_correct += found_first[index:]

            raise errors.EquationParseError(f'String `{found_first}`, followed by integer. Perhaps you ment "{possible_correct}"')

        presence = list()

        OPEN_BRACKETS = 0
        INDEX = 0
        SKIP_MANY = 0
        BRK_LAST = BREAK_ON_LAST

        for posfix in self.equation:

            if SKIP_MANY:

                if INDEX == (len(self.equation) - 1):
                    if OPEN_BRACKETS and self.equation[INDEX] == ')':
                        presence.append(Symbol(')'))
                        OPEN_BRACKETS -= 1

                SKIP_MANY -= 1
                INDEX += 1

                continue

            if posfix == '!':
                previous = presence[-1]
                if isinstance(previous, Operator):
                    raise errors.EquationParseError(f'Factorial used on `{previous.value}`')

                function = Function(factorial, ...)
                # Factorial marker has no inner parameter
                presence.append(function)

            elif posfix in ASCII_CHARS:
                INDEXED = ""
                FROM = self.equation[INDEX:]
                CURRENT_INDEX = 0

                MINI_SKIP = 0

                while True:
                    if MINI_SKIP:
                        MINI_SKIP -= 1
                        CURRENT_INDEX += 1
                        continue
                    ON_LAST = False

                    if CURRENT_INDEX > (len(FROM) - 1):
                        if BRK_LAST:
                            BRK_LAST = False
                            CURRENT_INDEX -= 1
                            ON_LAST = True
                        else:
                            break

                    sub_posfix = FROM[CURRENT_INDEX]

                    if sub_posfix in ASCII_CHARS and not ON_LAST:
                        INDEXED += sub_posfix
                    elif sub_posfix == " ":
                        pass
                    else:
                        try:
                            next_posfix = FROM[CURRENT_INDEX + 1]
                            if next_posfix in ASCII_CHARS:
                                nextASCII = True
                            else:
                                nextASCII = False
                        except IndexError:
                            nextASCII = False

                        if not nextASCII:

                            constant = abc.CONSTANTS.get(INDEXED)
                            func = abc.KEYWORDS.get(INDEXED)

                            if func and constant:
                                raise errors.EquationParseError(f'{INDEXED} is defined as both constant and function')
                            elif constant:
                                presence.append(Irrational(constant))
                                break

                            elif func:
                                FUNC_OPEN_BRACKS = 0

                                FUNC_EQ = ""
                                # Create sep equation obj to evaluate captured parameters
                                
                                TILL_END = self.equation[INDEX + CURRENT_INDEX:].strip()

                                if not TILL_END:
                                    raise errors.EquationParseError(f'"{INDEXED}" Called with no parameters')

                                if TILL_END.startswith('('):
                                    WRAPPED_IN_BRACKS = True
                                else:
                                    WRAPPED_IN_BRACKS = False

                                if WRAPPED_IN_BRACKS and not TILL_END.endswith(')'):
                                    if TILL_END[-2] == ')' and TILL_END[-1] == '!':
                                        pass
                                    else:
                                        raise errors.EquationParseError(f'"{INDEXED}" bracket was not closed')

                                for sub_sub_posfix in TILL_END:
                                    if sub_sub_posfix == ' ':

                                        if not WRAPPED_IN_BRACKS:
                                            break

                                        continue

                                    if sub_sub_posfix == '(':
                                        FUNC_EQ += '('
                                        FUNC_OPEN_BRACKS += 1

                                    if sub_sub_posfix == ')':
                                        if FUNC_OPEN_BRACKS < 1:
                                            OPEN_BRACKETS -= 1
                                            break
                                        
                                        FUNC_EQ += ')'
                                        FUNC_OPEN_BRACKS -= 1

                                    else:
                                        FUNC_EQ += sub_sub_posfix

                                    SKIP_MANY += 1

                                if FUNC_OPEN_BRACKS > 1:
                                    raise errors.EquationParseError(f"{FUNC_OPEN_BRACKS} unclosed brackets whilst parsing '{func.__qualname__}'")

                                if not FUNC_EQ.startswith('('):
                                    FUNC_EQ += ')'
                                    FUNC_EQ = '(' + FUNC_EQ

                                print(FUNC_EQ)

                                pre_presence = Equation(FUNC_EQ, *self.args, **self.kwargs)._sub(*args, **kwargs)
                                
                                FUNCTION = Function(
                                    INDEXED, pre_presence
                                )


                                presence.append(FUNCTION)

                                # presence.extend(pre_presence)
                                # FUNCTION basically has `pre_presence` in it, so this is pretty much useless

                                break

                            # Create unknown
                            unknown = Unknown(INDEXED)
                            presence.append(unknown)
                            break


                    SKIP_MANY += 1
                    CURRENT_INDEX += 1

            # Brackets
            if posfix == "(":
                SKIPPED = False

                if INDEX < (len(self.equation) - 1):
                    copy = self.equation[INDEX:]
                    COPY_INDEX = 0
                    COPY_OPEN_BRACKETS = 0

                    # Contains everythings out of the bracket
                    while True:

                        if not copy:
                            break
                        if COPY_INDEX > (len(copy) - 1):
                            break

                        if copy[COPY_INDEX] == '(':
                            COPY_OPEN_BRACKETS += 1
                            OPEN_BRACKETS += 1

                        if copy[COPY_INDEX] == ')':
                            COPY_OPEN_BRACKETS -= 1
                            OPEN_BRACKETS -= 1
                            
                            if not COPY_OPEN_BRACKETS:
                                break

                        COPY_INDEX += 1

                    copy = copy[:(COPY_INDEX + 1)]

                    try:
                        complex_ = Complex(raw=copy, check_value_attr=True)
                        SKIPPED = True
                        SKIP_MANY += len(copy)

                        presence.append(complex_)
                    except Exception:
                        if copy in ['(+|-)', '(-|+)']:
                            presence.append(PlusOrMinus())
                            SKIP_MANY += 5
                            SKIPPED = True
                        
                if not SKIPPED:
                    OPEN_BRACKETS += 1
                    presence.append(Symbol('('))

            elif posfix == ")":
                if OPEN_BRACKETS < 1:
                    raise errors.EquationParseError(f'Unexpected token `)`. At index `{INDEX}`')
                OPEN_BRACKETS -= 1
                presence.append(Symbol(')'))

            try:
                is_op = Operator(posfix)

                if INDEX < (len(self.equation) - 1):
                    is_double = self.equation[INDEX + 1]
                    try:
                        is_op = Operator((posfix + is_double))
                        SKIP_MANY += 1
                    except ValueError:
                        pass

                presence.append(is_op)

            except ValueError:
                pass

            if posfix.isdigit():
                current_pos = self.equation[INDEX:]
                CURRENT_INDEX = 0

                UNKNOWN = ""
                NUMBER = ""

                while True:
                    if CURRENT_INDEX > (len(current_pos) - 1):
                        break

                    sub_posfix = current_pos[CURRENT_INDEX]

                    if sub_posfix in ASCII_CHARS:
                        UNKNOWN += sub_posfix
                    elif sub_posfix.isdigit():
                        NUMBER += sub_posfix
                    elif sub_posfix == '.':
                        NUMBER += '.'
                    else:

                        break

                    CURRENT_INDEX += 1
                    SKIP_MANY += 1

                if UNKNOWN and NUMBER:
                    unknown_has_value = unknown_mapping.get(UNKNOWN)
                    if unknown_has_value:
                        u = convert_type(unknown_has_value)
                    else:
                        u = Unknown(UNKNOWN)

                    pre_presence = [
                        Symbol('('),
                        Irrational(NUMBER),
                        Operator('*'),
                        u,
                        Symbol(')')
                    ]
                    presence.extend(pre_presence)
                elif NUMBER:
                    presence.append(Irrational(NUMBER))
                elif UNKNOWN:
                    unknown_has_value = unknown_mapping.get(UNKNOWN)
                    if unknown_has_value:
                        u = convert_type(unknown_has_value)
                    else:
                        u = Unknown(UNKNOWN)

                    presence.append(u)

            INDEX += 1

        if OPEN_BRACKETS:
            raise errors.EquationParseError(f'{OPEN_BRACKETS} Unclosed Brackets')

        return presence

    def substitute(self, *args, **kwargs):
        """
        Supply values, or use pre-existing values to substitute into your equation.
        Returns the result of the evaluated equation

        Parameters
        ----------
        *args: :class:`~typing.Any`
            Arguments to supply in your equation
        **kwargs: :class:`~typing.Any`
            Keyworded arguments to supply into your equation.
        """
        raise NotImplementedError()

    def solve(self, *args, **kwargs):
        """
        Equals your equation to ``0`` and solves it mathmatically.

        Parameters
        ----------
        *args: :class:`~typing.Any`
            Arguments to supply in your equation
        **kwargs: :class:`~typing.Any`
            Keyworded arguments to supply into your equation.

            **Warning:** Unlike `*args`, this will overwrite all instances of an unknown
        """
        raise NotImplementedError()

    def wrap_all(self, operator: str, ending: str, *eq_args, **eq_kwargs) -> None:
        """
        Places the entire of your current equation into brackets and adds and operator with another query.

        Example
        ^^^^^^^
        .. code-block:: py

            >>> from cake import Equation
            >>> y = Equation("2x + 2")
            >>> y.wrap_all("*", "2")
            >>> y
            (2x + 2) * 2

        Parameters
        ----------
        operator: :class:`str`
            The operator to use with the ending, check out how the ``Operator`` class works for more details.
        ending: :class:`str`
            A seperate query to append onto the end
        *args: :class:`~typing.Any`
            Arguments for any new vars, its best to do ``list(Equation.args) + [...]``
        **kwargs: :class:`~typing.Any`
            Keyworded arguments, works the same way as `*args`, except is much easier to implement.
        """
        op = Operator(operator)

        eq = f'({self.__equation})'
        eq += f' {op.value} {ending}'

        self.__equation = eq

        self.update_variables(*eq_args, **eq_kwargs)

    def update_variables(self, overwrite: bool = True, *args, **kwargs) -> typing.Union[dict, None]:
        """
        Update the built in mapping for unknown values

        Paramters
        ---------
        overwrite: :class:`bool`
            Should overwrite the current mapping, or return the mapping which was just created.

            Defaults to ``True``.
        *args: :class:`~typing.Any`
            Arguments to replace, it works by adding new arguments to the start and trimming down the current args.

            So if you had ``10, 20`` as your arguments and you supply ``30`` it becomes ``30, 20``.
        **kwargs: :class:`~typing.Any`
            Keyworded arguments to change or add to your equation unknown mapping
        """

        current_args = self.args
        default_args = list(args) + current_args[len(args):]

        default_kwargs = {**self.kwargs, **kwargs}

        mapping = self._sort_values(*default_args, **default_kwargs)

        if overwrite:
            self.args = default_args
            self.kwargs = default_kwargs

            self.__mappings = mapping
        else:
            return mapping

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

        return repr(self.equation)
