import re
import typing
import string

from cake import abc, errors
import cake

from ..core.markers import Operator, Symbol, PlusOrMinus, FunctionMarker
from ..core.types.complex import Complex
from ..core.types.irrational import Irrational
from ..core.unknown import Unknown

from .equation import Equation
from ._ast import *
from cake.helpers import convert_type

# Imports for tokenizing
from tokenize import (
    tokenize,
    # IGNORE MARKERS
    ENDMARKER,
    NEWLINE,
    ENCODING,
    # MARKERS TO SEARCH
    OP,
    NAME,
    NUMBER,
    ERRORTOKEN,
)
from io import BytesIO

ASCII_CHARS = list(string.ascii_lowercase)
# Use lowercases so `X` is equal to `x`
BLACKLISTED = list(abc.KEYWORDS.keys()) + list(abc.CONSTANTS.keys())
# Keywords that cant be assigned to an unknown
VALID_SYMBOLS = {"!", "(", ")"}
# Used for parsing functions
IGNORE = (ENDMARKER, NEWLINE, ENCODING)
# Ignore any tokens from the tokenizer

################
#
# Regex patterns
#
################

FIND_UNKNOWNS = re.compile("[a-zA-Z]+", re.IGNORECASE)
# Looks for any letters, this is useful when mapping values to a specific unknown

INVALID_OPS = re.compile("[a-zA-Z]+[0-9]+", re.IGNORECASE)
# Looks for any incorrect patterns such as `sqrt4`

# Main Object
subExecGlobals = {'math': __import__('math'), 'cake': __import__('cake')}


class Expression(object):
    """
    Create simple mathmatical expressions and solve/substitute by providing values.
    If you supply an expression with multiple lines or as a list, it splits them and returns a list of expressions instead of a single expression object

    .. code-block:: py

        >>> from cake import Expression
        >>> circle, line = Expression(['(x ** 2) + (y ** 2)', '2x + y'])

    Parameters
    ----------
    expression: :class:`str`
        The statement used when processing your statement
    *default_args: :class:`~typing.Any`:
        Default set of arguments used when substituting the expression, IF they are not supplied during substitution.
        If you supply some, it skips the provided ones and uses the ones that havent been provided.

        .. code-block:: py

            >>> from cake import expression
            >>> y = expression("2x + 3", 1)
            >>> y._sub()
            [Symbol('('), Integer(1), ..., Operator(+), Integer(3)]

    **default_kwargs: :class:`~typing.Mapping[str, typing.Any]`
        A set of keyword arguments use when substituting the expression, IF they have not been supplied during substitution.
        Compared to ``default_args``, this allows you to choose which arguments to supply.

        .. code-block:: py

            >>> from cake import Expression
            >>> eq = Expression("x ** 2 + y ** 2")
            >>> eq._sub(y=10)
            [Unknown(x), ..., Operator(+), Integer(10), ...]

    """

    def __new__(
        cls, expression: typing.Union[str, list], *default_args, **default_kwargs
    ):
        multiple = expression.split("\n") if type(expression) == str else expression

        if multiple == Ellipsis:
            multiple = ""

        if len(multiple) > 1:
            eqs = list()

            for eq in multiple:
                eqs.append(Expression(eq, *default_args, **default_kwargs))
            return eqs

        return super(Expression, cls).__new__(
            Expression, *default_args, **default_kwargs
        )

    def __init__(
        self,
        expression: typing.Union[str, typing.BinaryIO],
        *default_args,
        **default_kwargs,
    ) -> None:
        default_args = list(default_args)

        if hasattr(expression, "seek"):
            self.__expression = expression.read().decode(
                encoding="ASCII", errors="ignore"
            )
        else:
            if expression == Ellipsis:
                expression = ""

            self.__expression = expression.lower()

        self.args = default_args
        self.kwargs = default_kwargs

        self.__mappings = self._sort_values(*default_args, **default_kwargs)

    def _sort_values(self, *args, **kwargs) -> dict:
        unknowns = FIND_UNKNOWNS.findall(self.__expression)
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

    def _sub(
        self,
        update_mappings: bool = False,
        return_tokens: bool = False,
        *args,
        **kwargs,
    ):
        """
        Simple tokenization, returns a list of tokens. This is usually only important for parsing.
        An example of this can be found in the ``substitution`` method.

        Parameters
        ----------
        update_mappings: :class:`bool`
            Update the inner unknown mappings with any new args or kwargs
        return_tokens: :class:`bool`
            Returns a tuple with ``(Evaluated_Tokens, Tokens)``
        *args, **kwargs: :class:`~typing.Any`
            Overwrites or adds to pre-existing inner mappings for unknown values
        """

        if update_mappings:
            self.update_variables(*args, **kwargs)
            unknown_mapping = self.__mappings
        else:
            unknown_mapping = self.update_variables(False, *args, **kwargs)

        invalid = INVALID_OPS.findall(self.expression)
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
            possible_correct += " "
            possible_correct += found_first[index:]

            raise errors.SubstitutionError(
                f'String `{found_first}`, followed by integer. Perhaps you ment "{possible_correct}"'
            )

        as_file = BytesIO(self.expression.encode(encoding="ASCII", errors="ignore"))

        as_file.seek(0)

        tokens = list(tokenize(as_file.readline))

        if not tokens:
            return []

        if tokens[0].type == ENCODING:
            tokens.pop(0)

        presence = list()

        OPEN_BRACKETS = 0
        ACTUAL_INDEX = 0
        TOKEN_INDEX = 0

        SKIP = 0

        while True:
            if TOKEN_INDEX > (len(tokens) - 1):
                break

            if SKIP:
                SKIP -= 1
                TOKEN_INDEX += 1
                continue

            token = tokens[TOKEN_INDEX]

            string = (token.string).lower()
            type_ = token.type

            if type_ in IGNORE:
                pass

            elif type_ == OP:
                if string == "(":
                    POS_TOKENS = tokens[TOKEN_INDEX:]

                    is_plus = POS_TOKENS[0:5]
                    to_mapping = "".join([i.string for i in is_plus])

                    if to_mapping in ["(+|-)", "(-|+)"]:
                        SKIP += 4
                        presence.append(PlusOrMinus())
                    else:
                        try:
                            comp = Complex(raw=to_mapping)
                            presence.append(comp)

                            SKIP += 4
                        except ValueError:
                            presence.append(Symbol("("))
                            OPEN_BRACKETS += 1

                elif string == ")":
                    if OPEN_BRACKETS < 1:
                        INCORRECT_BRACK_INDEX = token.start[1]

                        raise errors.SubstitutionError(
                            f"Unexpected `)` at index {INCORRECT_BRACK_INDEX}"
                        )

                    presence.append(Symbol(")"))
                    OPEN_BRACKETS -= 1

                else:
                    string_ = abc.MAP_OPERATORS.get(string, string)
                    # Get the operator or just return the same string

                    try:
                        op = Operator(string_)
                        presence.append(op)
                    except ValueError as e:
                        raise errors.SubstitutionError(
                            f"Unknown Operator: {string}"
                        ) from e

            elif type_ in [NAME, ERRORTOKEN]:
                # Keep hunting for letters
                TK_INDEX = (TOKEN_INDEX + 1)
                TOKENS = list()

                while True:
                    if TK_INDEX > len(tokens):
                        break
                    tk = tokens[TK_INDEX]
                    if tk.type == NAME:
                        TOKENS.append(tk)
                        SKIP += 1
                    else:
                        break

                    TK_INDEX += 1

                if TOKENS:
                    string = ' '.join(map(lambda _: _.string, TOKENS))

                constant = abc.CONSTANTS.get(string)
                function = abc.KEYWORDS.get(string)
                symbol_func = abc.SYMBOL_KW.get(string)
                map_op = abc.MAP_OPERATORS.get(string)

                # Check for lettering

                if len([i for i in (constant, function, symbol_func, map_op) if i is not None]) > 1:
                    raise errors.SubstitutionError(
                        f"{string} is defined as multiple keywords"
                    )

                elif constant:
                    presence.append(Irrational(constant))

                elif function:
                    POS_TOKENS = tokens[(TOKEN_INDEX + 1) :]
                    # Start from next posfix, else the `function` NAME gets caught

                    if not POS_TOKENS:
                        raise errors.SubstitutionError(
                            f"{string} Called with no parameters"
                        )

                    if POS_TOKENS[0].string == "(":
                        WRAPPED_IN_BRACKETS = True
                    else:
                        WRAPPED_IN_BRACKETS = False

                    if not WRAPPED_IN_BRACKETS:
                        _, COL = POS_TOKENS[0].start

                        EQ = self.expression[COL:]
                        EVALUATE = EQ.split(" ")[0]

                        TREE, TOKENS = Expression(EVALUATE)._sub(
                            return_tokens=True, **self._sort_values(*args, **kwargs)
                        )

                    else:
                        FUNQ_EQ = ""
                        BRACKS = 0

                        for POSFIX in POS_TOKENS:

                            if POSFIX.string == "(":
                                BRACKS += 1
                                FUNQ_EQ += " ( "
                            elif POSFIX.string == ")":
                                if BRACKS < 1:
                                    OPEN_BRACKETS -= 1
                                    presence.append(Symbol(")"))
                                    break
                                BRACKS -= 1
                                FUNQ_EQ += " ) "

                            else:
                                FUNQ_EQ += f" {POSFIX.string} "

                        if BRACKS > 1:
                            raise errors.SubstitutionError(
                                f"{BRACKS} Unclosed brackets whilst evaluating {function.__qualname__}"
                            )

                        TREE, TOKENS = Expression(FUNQ_EQ)._sub(
                            return_tokens=True, **self._sort_values(*args, **kwargs)
                        )

                    if not TREE:
                        raise errors.SubstitutionError(
                            f"{string} Called with no parameters"
                        )

                    func = FunctionMarker(function, TREE)
                    SKIP += len(TOKENS)
                    presence.append(func)

                elif symbol_func:
                    LAST_POSFIX = presence[-1]
                    func_name = symbol_func.__qualname__.title()

                    if isinstance(LAST_POSFIX, Operator):
                        raise errors.SubstitutionError(
                            f"{func_name} called on an operator ({LAST_POSFIX.value}), at index {token.start[1]}."
                        )

                    if isinstance(LAST_POSFIX, Symbol):
                        if LAST_POSFIX.value != ")":
                            raise errors.SubstitutionError(
                                f"{func_name} called on an open bracket, at index {token.start[1]}"
                            )

                        OPEN_BRACKS = 0
                        POS_INDEX = 0
                        POS_TOKENS = tokens[:TOKEN_INDEX][::-1]
                        # Searching Backwards
                        # Factorial will be at the beginning

                        for POS_TOKEN in POS_TOKENS:

                            string = POS_TOKEN.string

                            if string == ")":
                                OPEN_BRACKS += 1
                            elif string == "(":
                                OPEN_BRACKS -= 1

                                if OPEN_BRACKS < 1:
                                    break

                            POS_INDEX += 1

                        if OPEN_BRACKS:
                            raise errors.SubstitutionError(
                                f'{OPEN_BRACKS} Unclosed brackets whilst evalutating "{symbol_func.__qualname__}"'
                            )

                        POS_TOKENS = POS_TOKENS[::-1]
                        PS_IND = (len(POS_TOKENS) - 1) - POS_INDEX

                        # Flip them back around

                        as_eq = [i.string for i in POS_TOKENS[PS_IND:]]

                        del presence[
                            ((TOKEN_INDEX - POS_INDEX) - 1) : (TOKEN_INDEX + 1)
                        ]

                        TREE = Expression(" ".join(as_eq))._sub(
                            **self._sort_values(*args, **kwargs)
                        )

                        func = FunctionMarker(symbol_func, TREE)
                        presence.append(func)

                    else:
                        new_pre = [Symbol("("), LAST_POSFIX, Symbol(")")]

                        func = FunctionMarker(symbol_func, new_pre)

                        presence[-1] = func

                elif map_op:
                    presence.append(Operator(map_op))

                else:
                    if string in unknown_mapping:
                        presence.append(convert_type(unknown_mapping[string]))

                    elif not (string in ASCII_CHARS):
                        # xy -> (x * y)
                        cd = '('
                        for st in string:
                            if st in unknown_mapping:
                                cd += str(unknown_mapping[st])
                            else:
                                if st not in ASCII_CHARS:
                                    raise errors.SubstitutionError(
                                        f"Unknown Token ({string}) at index {token.start[1]}"
                                    )
                                cd += st
                            cd += ' * '
                        cd = cd[:-3] + ')'
                        # Remove the ` * ` at the end

                        presence.extend(Expression(cd, *self.args, **self.kwargs)._sub(
                            update_mappings,
                            *args, **kwargs))
                    else:
                        presence.append(Unknown(string))

            elif type_ == NUMBER:
                POS_TOKENS = tokens[TOKEN_INDEX:]
                CURRENT_NUMBER = convert_type(string)

                if not POS_TOKENS:
                    presence.append(CURRENT_NUMBER)
                else:
                    NEXT = POS_TOKENS[1]

                    if NEXT.type == NAME:
                        constant = abc.CONSTANTS.get(NEXT.string)
                        function = abc.KEYWORDS.get(NEXT.string)

                        value = unknown_mapping.get(NEXT.string)
                        unk = Unknown(NEXT.string)

                        if value:
                            value = convert_type(value)
                        else:
                            value = unk

                        if constant:
                            SKIP += 1
                            presence.append(Irrational(constant))

                        elif not function:
                            SKIP += 1

                            presence.extend(
                                [
                                    Symbol("("),
                                    CURRENT_NUMBER,
                                    Operator("*"),
                                    value,
                                    Symbol(")"),
                                ]
                            )

                        else:
                            possible_correct = f"{string} * {NEXT.string}"

                            raise errors.SubstitutionError(
                                f'Invalid use of function "{function.__qualname__}" at index {NEXT.start[1]}. Perhaps you ment "{possible_correct}"'
                            )

                    else:
                        presence.append(CURRENT_NUMBER)

            else:

                # Stops `' '` from raising an error
                if string.strip():
                    raise errors.SubstitutionError(
                        f"Unknown Token ({string}) at index {token.start[1]}"
                    )

            ACTUAL_INDEX += len(string)
            TOKEN_INDEX += 1

        if OPEN_BRACKETS > 1:
            raise errors.SubstitutionError(f"{OPEN_BRACKETS} Unclosed brackets")

        if return_tokens:
            return presence, tokens
        return presence

    def _glSubCode(self, update_mapping: bool = False, *args, **kwargs):
        """
        Convert your expression into modern pythonic code, using the `Cake` library.
        If you want the answer directly, its best to use the `.substitute` method.

        Parameters
        ----------
        update_mapping: :class:`bool`
            Update the inner unknown mappings with any new args or kwargs
        *args: :class:`~typing.Any`
            Arguments to supply in your expression
        **kwargs: :class:`~typing.Any`
            Keyworded arguments to supply into your expression.
        """

        if "dirty" in kwargs:
            dirty = True
            vars = kwargs.pop('vars')
        else:
            vars = list()
            dirty = False

        presence = kwargs.pop('dirty', self._sub(update_mapping, *args, **kwargs))
        code = str()
        VARS = vars
        pm = 0

        for posfix in presence:
            if isinstance(posfix, Unknown):
                if posfix.value not in VARS:
                    VARS.append(f"{posfix.value} = Unknown('{posfix.value}')")
                code += f'({posfix.value})'

            elif isinstance(posfix, FunctionMarker):
                func, dirtyTokens = posfix.value
                evaluated = Expression(...)._glSubCode(*args, **{**kwargs, 'dirty': dirtyTokens, 'vars': VARS})

                newVars, evaluated, _ = evaluated
                VARS.extend(newVars)
                VARS = list(set(VARS))

                code += f"({func.__qualname__}({evaluated}))"

            elif isinstance(posfix, cake.Number):
                code += f'({posfix.__class__.__name__}({posfix.value}))'

            elif isinstance(posfix, PlusOrMinus):
                code += '(+|-)'     # This gets sorted out later
                pm += 1

            elif isinstance(posfix, (Symbol, Operator)):
                posfix.validate

                code += f'{posfix.value}'

        if not dirty:
            return "{}\n{}".format('\n'.join(VARS), code), pm
        return VARS, code, pm

    def convertToCode(self, update_mapping: bool = False, imports: tuple = tuple(), *args, **kwargs):
        """
        Convert your expression into executable code!

        .. warning::
            Any imports provided, can overwrite imports from the cake library!

        .. code-block:: py

            >>> from cake import Expression
            >>> imports = ("math *",)
            # Imports * from math
            # "math tan" only imports tan
            # "math (tan, sin)" only imports tan, sin
            >>> expr = "x + sqrt(y)"
            >>> Expr = Expression(expr)
            >>> Expr.convertToCode(imports=imports)
            ...

        Parameters
        ----------
        update_mapping: :class:`bool`
            Update the inner unknown mappings with any new args or kwargs
        imports: :class:`tuple`
            A tuple with import statements to be used when generating your code.
        """
        beginning = GEN_AUTO_CODE_MARKING(*imports)
        code, _ = self._glSubCode(update_mapping, *args, **kwargs)

        return f'{beginning}{code}'

    def substitute(self, update_mapping: bool = False, imports: tuple = tuple(), *args, **kwargs):
        """
        Sub values into your equation, and evaluates the expr.
        
        If your using the `(+|-)` op, it will return the result as a tuple. Else just the value.
        The length of the tuple varies in length, for every plus/minus op just multiply your value by `* 2` 

        Parameters
        ----------
        update_mapping: :class:`bool`
            Update the inner unknown mappings with any new args or kwargs
        *args: :class:`~typing.Any`
            Arguments to supply in your expression
        **kwargs: :class:`~typing.Any`
            Keyworded arguments to supply into your expression.
        """

        _, pmCount = self._glSubCode(update_mapping, *args, **kwargs)
        code = self.convertToCode(update_mapping, imports, *args, **kwargs)
        combos = cake.getPlusMinusCombos(pmCount)

        if not combos:
            return execCode(code)
        toBeEvaluated = list()

        for combo in combos:
            codeCopy = code
            for symbol in combo:
                ind = codeCopy.find('(+|-)')

                cmCopy = list(codeCopy)
                cmCopy[ind:(ind + 5)] = symbol
                # ind -> the first bracket
                # (ind + 5) -> captures remaining `+|-)`
                codeCopy = ''.join(cmCopy)
            toBeEvaluated.append(codeCopy)

        results = list()

        for rCode in toBeEvaluated:
            results.append(execCode(rCode))
        return tuple(results)

    def solve(self, *args, **kwargs):
        """
        Equals your expression to ``0`` and solves it mathmatically.

        Parameters
        ----------
        *args:
            Arguments to supply in your expression
        **kwargs:
            Keyworded arguments to supply into your expression.
        """
        raise NotImplementedError()

    def append(self, expr: typing.Union[str, "Expression"]) -> None:
        """
        Add a new expression onto your current expression

        .. code-block:: py

            >>> from cake import Expression
            >>> y = Expression("2x + 2")
            >>> y.append(" * 2")
            >>> y
            2x + 2 * 2

        Parameters
        ----------
        expr: :class:`~typing.Union[str, Expression]`
            The expression to append
        """
        if isinstance(expr, Expression):
            expr = Expression.expression
        self.__expression += expr

    def prepend(self, expr: typing.Union[str, "Expression"]) -> None:
        """
        Add a new expression to the beginning of your current expression.

        .. code-block:: py

            >>> from cake import Expression
            >>> y = Expression("2x + 2")
            >>> y.prepend("2 *")
            >>> y
            2 * 2x + 2

        Parameters
        ----------
        expr: :class:`~typing.Union[str, Expression]`
            The expression to prepend
        """
        if isinstance(expr, Expression):
            expr = Expression.expression
        self.__expression = expr + self.__expression

    def wrap_all(self, operator: str, ending: str, *eq_args, **eq_kwargs) -> None:
        """
        Places the entire of your current expression into brackets and adds and operator with another query.

        .. code-block:: py

            >>> from cake import Expression
            >>> y = Expression("2x + 2")
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
            Arguments for any new vars
        **kwargs: :class:`~typing.Any`
            Keyworded arguments, works the same way as `*args`, except is much easier to implement.
        """
        op = Operator(operator)

        eq = f"({self.__expression})"
        eq += f" {op.value} {ending}"

        self.__expression = eq

        self.update_variables(*eq_args, **eq_kwargs)

    def update_variables(
        self, overwrite: bool = True, *args, **kwargs
    ) -> typing.Union[dict, None]:
        """
        Update the built in mapping for unknown values

        Parameters
        ----------
        overwrite: :class:`bool`
            Should overwrite the current mapping, or return the mapping which was just created.

            Defaults to ``True``.
        *args: :class:`~typing.Any`
            Arguments to replace, it works by adding new arguments to the start and trimming down the current args.

            So if you had ``10, 20`` as your arguments and you supply ``30`` it becomes ``30, 20``.
        **kwargs: :class:`~typing.Any`
            Keyworded arguments to change or add to your expression unknown mapping
        """

        current_args = self.args
        default_args = list(args) + current_args[len(args) :]

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
        """Returns a copy of the variable mappings for unknowns"""
        return cake.copy(self.__mappings)

    @property
    def expression(self):
        """Returns a copy of the expression used when initialsing the class"""
        return self.__expression

    def __repr__(self) -> str:
        """
        Returns the expression set when initialising the class
        """

        return self.expression

    def __eq__(self, other: "Expression") -> "Equation":
        """
        Equality is not used for checking with an `Expression`.
        This instead creates an ``Equation`` object, which states:
            Expr1 = Expr2
        """
        raise NotImplementedError()
