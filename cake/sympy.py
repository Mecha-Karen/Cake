# SymPy Integrations
# - No code from sympy has been used, just copying the concept
# Link: https://github.com/sympy/sympy

from cake import (
    Unknown
)


def symbol(*symbols: str) -> tuple:
    if not symbols:
        return tuple()
    if len(symbols) == 1:
        symb = symbols[0]

        is_sep_by_comma = symb.split(', ')
        if len(is_sep_by_comma) == 1:
            symbols = symb.split(' ')
        else:
            symbols = is_sep_by_comma
    unknowns = list()

    for symbol in symbols:
        unknowns.append(Unknown.parse(symbol))

    return tuple(unknowns)
