import typing
import string
from math import pi, e

# Types
class IntegerType(typing.Protocol):
    def __int__(self) -> int:
        ...


class FloatType(typing.Protocol):
    def __float__(self) -> float:
        ...


class ComplexType(typing.Protocol):
    def __complex__(self) -> complex:
        ...


OPERATORS     = {"+", "-", "/", "*", "**", "^", "//", "&", ">>", "<<", "|"}
ASCII_CHARS   = list(string.ascii_letters)
INF_VALUE     = float('inf')
NEG_INF_VALUE = float('-inf')
NAN_VALUE     = float('nan')

MAP_OPERATORS = {
    "add": "+",
    "plus": "+",
    "subtract": "-",
    "minus": "-",
    "divide": "/",
    "multiply": "*",
    "times by": "*",
    "to the power of": "**",
    "raised to": "**",
    "floor division": "//",
    "modulus": "%",
}

ODD_NUMBERS: typing.Iterable[int] = filter(lambda _: _ % 2 != 0, range(100))
