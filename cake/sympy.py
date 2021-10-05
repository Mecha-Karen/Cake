# SymPy Integrations
# - No code from sympy has been used, just using method names
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
        # unknowns.append(Unknown.parse(symbol))
        # not implemented yet

        unknowns.append(Unknown(symbol))

    if len(unknowns) > 1:
        return tuple(unknowns)
    return unknowns[0]

# Some people may like the plural
symbols = symbol
