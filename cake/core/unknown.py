from math import factorial as fc
from cake.abc import PRETTY_PRINT_SYMBOLS, UNKNOWN_PRETTIFIER_SYMBOL


class Unknown(object):
    """
    An object representing an unknown value
    """
    def __init__(
        self, value: str, *,
        raised_to: int = 1, 
        factorial: bool = False, sqrt: bool = False
    ):

        self.value = value

        self.raised = raised_to
        self.factorial = bool(factorial)
        self.sqrt = bool(sqrt)

    def multiply(self, other):
        raise NotImplementedError()

    def add(self, other):
        raise NotImplementedError()

    def floordiv(self, other):
        raise NotImplementedError()

    def divmod(self, other):
        raise NotImplementedError()

    def mod(self, other):
        raise NotImplementedError

    def truediv(self, other):
        raise NotImplementedError()

    def pow(self, other):
        raise NotImplementedError()

    def lshift(self, other):
        raise NotImplementedError()

    def rshift(self, other):
        raise NotImplementedError()

    def _and(self, other):
        raise NotImplementedError() 

    def xor(self, other):
        raise NotImplementedError()

    def _or(self, other):
        raise NotImplementedError()

    def __repr__(self) -> str:
        value = self.value

        if self.sqrt:
            value = '√' + value

        if self.raised and str(self.raised) != '1':
            squares = ''
            for sq in str(self.raised):
                sym = PRETTY_PRINT_SYMBOLS['powers'].get(sq, UNKNOWN_PRETTIFIER_SYMBOL)
                squares += sym

            value += squares

        if self.factorial:
            value += '!'

        return f'Unknown({value})'
