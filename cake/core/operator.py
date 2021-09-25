from cake.abc import OPERATORS, MAP_OPERATORS

class Operator(object):
    __slots__ = ('value')

    def __init__(self, op: str) -> None:
        self.value = MAP_OPERATORS.get(op.lower()) or op

        if not self.value in OPERATORS:
            raise TypeError('%s is not a valid operator' % self.op)

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
    def eval(self):
        return self.evaluate
