# Functions from `mpmath` tailor made to handle our matrix objects
# Original Source: https://github.com/fredrik-johansson/mpmath/blob/master/mpmath/matrices/linalg.py

from mpmath import (
    absmin, eps, fsum, inf
)
from cake.helpers import copy

__all__ = ("mnorm", "_BC_DET")


def mnorm(M, p: int = 1):
    n, m = M.dimensions
    if p == 1:
        return max(fsum((M.matrix[i][j] for i in range(m)), absolute=1) for j in range(n))
    elif p == inf:
        return max(fsum((M.matrix[i][j] for j in range(n)), absolute=1) for i in range(m))
    else:
        raise NotImplementedError("matrix p-norm for arbitrary p")


def _BC_DET(M, *, cache: bool = False) -> tuple:
    if (M.dimensions[0] != M.dimensions[1]) or M.dimensions == (1, 1) or not M.matrix:
        raise ValueError(f'Non-square matrixes cannot have a determinant')

    if cache and getattr(M, 'c_dt', None):
        return M.c_dt
    orig = M
    M = M.copy()

    tol = absmin(mnorm(M, 1) * eps)
    rows = M.rows
    p = [None] * (rows - 1)
    for i in range(rows - 1):
        biggest = 0

        for j in range(i, rows):
            s = fsum([absmin(M.matrix[j][l]) for l in range(i, rows)])
            if absmin(s) <= tol:
                raise ZeroDivisionError(f'Matrix is numerically singular')
            current = 1 / s * absmin(M.matrix[j][i])
            if current > biggest:
                biggest = current
                p[i] = j

        M.swaprow(i, p[i])

        if absmin(M.matrix[i][i]) <= tol:
            raise ZeroDivisionError(f'Matrix is numerically singular')
        for k in range(i + 1, rows):
            M.matrix[k][i] /= M.matrix[i][i]
            for m in range(i + 1, rows):
                M.matrix[k][m] -= M.matrix[k][i] * M.matrix[i][m]
    
    if absmin(M.matrix[rows - 1][rows - 1]) <= tol:
        raise ZeroDivisionError(f'Matrix is numerically singular')

    if cache:
        orig.c_dt = (orig, M, p)
    return orig, M, p


def lSolve(M, b, p = None):
    if M.dimensions[0] != M.dimensions[1]:
        raise ValueError('Need a `n*n` matrix')
    rows = M.rows

    if len(b) != rows:
        raise ValueError('Value should be equal to N')
    b = copy(b)

    if p:
        for i in range(1, rows):
            ...
