# Shortcuts for creating different matrixes

import cake
import random as rd


def randomMatrix(col: int, row: int) -> "cake.Matrix":
    """
    Returns a matrix with random numbers

    Parameters
    ----------
    col: :class:`int`
        How many columns the matrix should have
    row: :class:`int`
        How many rows the matrix should have
    """
    return cake.Matrix(*[[rd.randint() for j in range(row)] for i in range(col)])
