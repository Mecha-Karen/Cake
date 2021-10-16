# Shortcuts for creating different matrixes

import typing
import cake
import random as rd


def randomMatrix(col: int = 3, row: int = 3, _range: typing.Tuple[int] = (0, 100)) -> "cake.Matrix":
    """
    Returns a matrix with random numbers

    Parameters
    ----------
    col: :class:`int`
        How many columns the matrix should have
        Defaults to ``3``
    row: :class:`int`
        How many rows the matrix should have
        Defaults to ``3``
    _range: :class:`tuple`:
        A tuple with 2 values, denoting the start and end for the random number selection.
        Defaults to ``(0, 100)``
    """
    return cake.Matrix(*[[rd.randint(*_range) for j in range(row)] for i in range(col)])


def identityMatrix(col: int = 3, row: int = 3) -> "cake.Matrix":
    """
    Returns an indentity/eye matrix

    Parameters
    ----------
    col: :class:`int`
        How many columns the matrix should have
        Defaults to ``3``
    row: :class:`int`
        How many rows the matrix should have
        Defaults to ``3``
    """
    return randomMatrix(col, row).identity()
