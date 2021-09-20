from cake.abc import OPERATORS


class Operator(object):
    __slots__ = ('op')

    def __init__(self, op: str) -> None:
        self.op = op

        if not self.op in OPERATORS:
            raise TypeError('%s is not a valid operator' % self.op)

    def __repr__(self) -> str:
        return f"Operator({self.op})"

    def evaluate(self, left, right):
        r"""
        Shortcut method of evaluating simple queries
        """
        if not self.op in OPERATORS:
            raise TypeError('%s is not a valid operator' % self.op)

        exec(f"""locals()['temp'] = {left} {self.op} {right}""")
        return locals()['temp']

    @property
    def eval(self):
        return self.evaluate
