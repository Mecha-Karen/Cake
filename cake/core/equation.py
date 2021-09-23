import math
import string

ASCII_CHARS = string.ascii_letters


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

        Example
        -------

        .. code-block:: py

            >>> from cake import Equation
            >>> eq = Equation("x ** 2 + y ** 2").bidmas()
            >>> eq
            "(x ** 2) + (y ** 2)"
            >>> eq._sub(y=10)
            [Unknown(x), Operator(+), Integer(y)]

    
    """

    def __init__(self, equation: str, *default_args, **default_kwargs) -> None:
        default_args = list(default_args)

        self._eq = list(equation)
        self.equation = equation
        self.defaults = default_args
        self.kwargs = default_kwargs

        self.posfix = {}

        for i in range(len(equation)):
            char = equation[i]
            if char in ASCII_CHARS:
                is_kwarg = default_kwargs.get(char)
                if is_kwarg:
                    self.posfix[i] = is_kwarg
                else:
                    if default_args:
                        default_val = default_args.pop(0)
                        self.posfix[i] = default_val

        for index, value in self.posfix.items():
            self._eq[index] = value
        self._eq = list(filter(lambda element: element != ' ', self._eq))

    def _sub(self, *args, **kwargs):
        """
        Substitute values into your equation, and return a list containing your parsed equation.
        For solving it is recomended to use ``solve`` instead of this if your intending to solve the result.

        Parameters
        ----------

        *args: :class:`~typing.Any`
            A set of arguments to substitute into your equation
        **kwargs: :class:`~typing.Mapping[str, typing.Any]`
            A set of keyword arguments to substitute into your equation.
            Keyword provided replaces the one in the equation e.g. `x=10` replaces only x.

        Returns
        -------
        :class:`list`
        """

        args = list(args)

        def inner(element):
            if element in kwargs:
                return kwargs[element]
            if args and (str(element) in ASCII_CHARS):
                return args.pop(0)
            return element

        return list(map(inner, self._eq))

    def __repr__(self) -> str:
        """
        Returns the equation set when initialising the class
        """

        return self.equation
