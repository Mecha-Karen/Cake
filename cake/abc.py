import math
import typing

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


OPERATORS: typing.Set[str] = {"+", "-", "/", "*", "**", "^", "//", "&", ">>", "<<", "|"}

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

KEYWORDS: typing.Mapping[str, typing.Callable] = {
    "sqrt": math.sqrt,
    "sin": lambda degrees: math.sin(math.radians(degrees)),
    "cos": lambda degrees: math.cos(math.radians(degrees)),
    "tan": lambda degrees: math.tan(math.radians(degrees)),
    "cot": lambda degrees: 1 / (math.tan(math.radians(degrees))),
    "sec": lambda degrees: 1 / (math.cos(math.radians(degrees))),
    "cosec": lambda degrees: 1 / (math.sin(math.radians(degrees))),
}

SYMBOL_KW: typing.Mapping[str, typing.Callable] = {"!": math.factorial}

CONSTANTS: typing.Mapping[str, IntegerType] = {"pi": math.pi, "e": math.e}

SCALES: typing.Mapping[str, int] = {
    "hundred": 1 * (10 ** 2),
    "thousand": 1 * (10 ** 3),
    "million": 1 * (10 ** 6),
    "billion": 1 * (10 ** 9),
    "trillion": 1 * (10 ** 12),
}

NUMBERS: typing.Mapping[str, int] = (
    {
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
)

ODD_NUMBERS: typing.Iterable[int] = filter(lambda _: _ % 2 != 0, range(100))

# Prettifiers
PRETTY_PRINT_SYMBOLS = {
    "sqrt": "√",
    "pi": "π",
    "e": "e",
    "powers": {
        "0": "⁰",
        "1": "¹",
        "2": "²",
        "3": "³",
        "4": "⁴",
        "5": "⁵",
        "6": "⁶",
        "7": "⁷",
        "8": "⁸",
        "9": "⁹",
        "+": "⁺",
        "-": "⁻",
        "(": "⁽",
        ")": "⁾",
        "n": "ⁿ",
    },
}

UNKNOWN_PRETTIFIER_SYMBOL = "?"
