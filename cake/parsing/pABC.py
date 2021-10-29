from ..functions.basic.trig import *
from ..functions.basic.elem import *
import typing
from cake.abc import IntegerType, pi, e


KEYWORDS: typing.Mapping[str, typing.Callable] = {
    "sqrt": Sqrt,
    "sin": Sin,
    "cos": Cos,
    "tan": Tan,
    "cot": Cot,
    "sec": Sec,
    "cosec": Cosec,
}

SYMBOL_KW: typing.Mapping[str, typing.Callable] = {
    "!": Factorial
}

CONSTANTS: typing.Mapping[str, IntegerType] = {"pi": pi, "e": e}

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