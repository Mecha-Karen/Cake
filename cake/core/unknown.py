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

    def divmod(self, other):
        raise NotImplementedError()

