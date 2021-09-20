class Unknown(object):
    """
    An object representing an unknown value
    """
    def __init__(
        self, value: str, *,
        square: int, 
    ):
        self.value = value
        self.square = square

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
