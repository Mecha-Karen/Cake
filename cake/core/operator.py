class Operator(object):
    __slots__ = ('op')

    def __init__(self, *, op: str) -> None:
        self.op = op

    def evaluate(self, left, right):
        result = exec(f'x {self.op} y', {'x': left, 'y': right})
        return result
