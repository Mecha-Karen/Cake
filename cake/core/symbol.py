ALLOWED = {
    "(", ")", "{", "}", "[", "]",
}

class Symbol(object):
    """
    A basic object which works like, Operator. This servers no purpose but to act as a marker for substitution and argument parsing.
    """

    __slots__ = ('value')

    def __init__(self, symbol: str) -> None:
        if not symbol in ALLOWED:
            raise TypeError('Incorrect symbol provided, please choose from\n%s' % ', '.join(ALLOWED))

        self.value = symbol
