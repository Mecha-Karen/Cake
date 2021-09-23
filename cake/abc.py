import math
import typing

# Types
NUMBER = typing.TypeVar('NUMBER', int, float, complex)

OPERATORS: typing.Set[str] = {
    "+", "-", "/", "*", "**", "^",
    "//", "&", ">>", "<<", "|"
}

KEYWORDS: typing.Mapping[str, typing.Callable[[NUMBER], NUMBER]] = {
    "!": math.factorial,
    "sqrt": math.sqrt,
}

CONSTANTS: typing.Mapping[str, NUMBER] = {
    'pi': math.pi,
    'e': math.e
}

SCALES: typing.Mapping[str, int] = {
    "hundred": 1 * (10 * 2),
    "thousand": 1 * (10 * 3),
    "million": 1 * (10 ** 6),
    "billion": 1 * (10 ** 9),
    "trillion": 1 * (10 ** 12),
}

NUMBERS: typing.Mapping[str, int] = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
    "ten": 10,
    "eleven": 11,
    "twelve": 12,
    "thirteen": 13,
    "fourteen": 14,
    "fifteen": 15,
    "sixteen": 16,
    "seventeen": 17,
    "eighteen": 18,
    "nineteen": 19,
    "twenty": 20,
    "thirty": 30,
    "forty": 40,
    "fifty": 50,
    "sixty": 60,
    "seventy": 70,
    "eighty": 80,
    "ninety": 90,
},

ODD_NUMBERS: typing.Iterable[int] = filter(lambda _: _ % 2 != 0, range(100))


class IntegerType(typing.Protocol):
    def __int__(self) -> int: ...
