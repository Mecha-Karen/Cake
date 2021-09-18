import math
import string

ASCII_CHARS = string.ascii_letters


class Equation(object):
    def __init__(self, equation: str, *default_args, **default_kwargs):
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

    def sub(self, *args, **kwargs):
        args = list(args)

        def inner(element):
            if element in kwargs:
                return kwargs[element]
            if args and (str(element) in ASCII_CHARS):
                return args.pop(0)
            return element

        return list(map(inner, self._eq))

    def __repr__(self) -> str:
        return self.equation
