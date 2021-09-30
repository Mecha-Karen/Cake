import typing
from cake.abc import OPERATORS, MAP_OPERATORS

ALLOWED = {
    "(", ")", "{", "}", "[", "]",
}


class Marker(object):
    """
    An object which used to seperate and tidy up Equations.
    This serves no real purpose but to help with tagging.

    Parameters
    ---------
    value: :class:`str`
        The value of the marker
    """
    __slots__ = ('value')

    def __init__(self, value: str) -> None:
        self.value = value

    def __repr__(self) -> str:
        return f"Marker({self.value})"


class Symbol(Marker):
    def __init__(self, value: str) -> None:
        if value not in ALLOWED:
            raise ValueError('Invalid symbol provided! Choose from:\n{}'.format(', '.join(ALLOWED)))

        super().__init__(value)

    @property
    def validate(self) -> typing.Optional[bool]:
        if super().value not in ALLOWED:
            raise ValueError('%s is not a valid symbol' % super().value)
        return True

    def __repr__(self) -> str:
        # Wrapped with `'` so you can actually see it.
        return f"Symbol('{super().value}')"


class Operator(Marker):
    def __init__(self, op: str) -> None:
        op = MAP_OPERATORS.get(op.lower()) or op

        if not op in OPERATORS:
            raise ValueError('%s is not a valid operator' % op)

        super().__init__(op)

    def __repr__(self) -> str:
        return f"Operator({self.value})"

    def evaluate(self, left, right):
        r"""
        Shortcut method of evaluating simple queries
        """

        if not self.value in OPERATORS:
            raise TypeError('%s is not a valid operator' % self.value)

        exec(f"""locals()['temp'] = {left} {self.value} {right}""")
        return locals()['temp']

    @property
    def validate(self) -> typing.Optional[bool]:
        op = super().value

        op = MAP_OPERATORS.get(op.lower()) or op

        if not op in OPERATORS:
            raise TypeError('%s is not a valid operator' % op)
        return True

    @property
    def eval(self):
        return self.evaluate

class PlusOrMinus(Marker):
    def __init__(self) -> None:
        super().__init__('+-')

    def __repr__(self) -> str:
        return f"Operator(+/-)"

class Function(Marker):
    def __init__(self, function: str, inter: typing.Any) -> None:
        super().__init__(
            (function, inter)
        )

    def __repr__(self) -> str:
        function, inter = super().value
        return f"Function(name={function}, value={inter})"
