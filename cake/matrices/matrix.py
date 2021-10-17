from __future__ import annotations

from cake.abc import IntegerType
import cake

from copy import deepcopy
import typing
from mpmath import (
    absmin, eps, fsum, inf
)

# Implemenation of `mpmath.mnorm`
def mnorm(M, p: int = 1):
    n, m = M.dimensions
    if p == 1:
        return max(fsum((M.matrix[i][j] for i in range(m)), absolute=1) for j in range(n))
    elif p == inf:
        return max(fsum((M.matrix[i][j] for j in range(n)), absolute=1) for i in range(m))
    else:
        raise NotImplementedError("matrix p-norm for arbitrary p")

class Matrix:
    """
    Matrixes are an array of numbers.

    Example
    ^^^^^^^
    .. code-block:: py

        >>> from cake import Matrix
        >>> x = Matrix([1, 2, 3], [1, 2, 3])
        >>> x + Matrix([1, 2, 3], [1, 2, 3])
        ([2, 4, 6], [2, 4, 6])

    Parameters
    ----------
    *rows: :class:`~typing.List[int]`
        A list of rows, the length of each row MUST be the same.
        The length of the row becomes the column length and then amount of rows you give becomes the 
    """

    def __init__(self, *rows):
        from cake import convert_type

        if not rows:
            self.matrix = []
        else:
            if len(rows) == 1 and isinstance(rows[0][0], (list, tuple)):
                rows = rows[0]

            if any(i for i in rows if len(i) < len(rows[0])):
                raise ValueError('Row lengths in matrix not equal')

            self.matrix = list(rows)

        self.cols = len(rows[0])
        self.rows = len(rows)

    def copy(self) -> Matrix:
        """ Return a copy of the current matrix """
        return deepcopy(self)

    def get_row(self, row_number: int) -> list:
        """
        Get a specific row from the matrix

        Parameters
        ----------
        row_number: :class:`int`
            The specific row to fetch
        """
        return self.matrix[row_number]

    def get_column(self, col_number: int) -> int:
        """
        Get a specific column from the matrix

        Parameters
        ----------
        row_number: :class:`int`
            The specific column to fetch
        """
        data = list()

        for row in self.matrix:
            data.append(row[col_number])

        return data

    def transpose(self) -> Matrix:
        """
        Transpose the matrix
        """
        data = self.matrix
        ret = [[data[x][y] for x in range(len(data))] for y in range(len(data[0]))]

        return Matrix(*ret)

    def identity(self, *, join: bool = False) -> Matrix:
        """
        Returns the identity of the matrix, useful for inverting matrixes

        Parameters
        ----------
        join: :class:`bool`
            Whether to return the matrix with the identity on the left, joined with the original matrix
        """
        CUR_COL = 1
        MATRIX = [list() for i in range(self.rows)]

        for i in range(self.rows):
            
            # Why do we not do `self.cols` instead of `self.rows` here
            # Well simply, indentiy matrixes will always be a square
            for j in range(self.rows):
                if (j + 1) == CUR_COL:
                    MATRIX[i].append(1)
                else:
                    MATRIX[i].append(0)
            CUR_COL += 1
        
        if join:
            return Matrix(
                *[self.matrix[i] + MATRIX[i] for i in range(self.rows)]
            )
        return Matrix(*MATRIX)

    def inverse(self) -> Matrix:
        """
        Get the inverse of the matrix. Uses the Gauss–Jordan elimination method.
        """
        if self.determinant() == 0:
            raise ValueError('Determinant is zero, therefore inverse matrix doesn\'t exist')

        raise NotImplementedError()

    def determinant(self, *, cache: bool = False) -> int:
        if any(i for i in self.matrix if cake.Unknown in [type(i) for j in i]):
            raise ValueError('Cannot work out determinant of matrix as unknown value is present')

        try:
            R, p, orig = _BC_DET(self.copy(), cache=cache)
        except ZeroDivisionError:
            return 0
        z = 1
        for i, e in enumerate(p):
            if i != e:
                z *= -1
        for i in range(self.rows):
            z *= R.matrix[i][i]
        return z

    def swaprow(self, i, j):
        """
        Swap 2 rows

        Parameters
        ----------
        i: :class:`int`
            The row to be swapped with j
        j: :class:`int`
            The row to be swapped with i
        """
        r1 = self.get_row(i)
        r2 = self.get_row(j)

        self.matrix[i] = r2
        self.matrix[j] = r1

    def convert_types(self) -> Matrix:
        """
        Converts the elements in the matrix to cake objects if possible
        """
        return Matrix(*[list(map(cake.convert_type, i)) for i in self.matrix])

    def __add__(self, other: typing.Union[IntegerType, Matrix]) -> Matrix:
        rows = list()

        if isinstance(other, Matrix) and ((other.rows != self.rows) or (other.cols != self.cols)):
            raise ValueError('Provided matrix has not got the same dimensions')

        for i in range(self.rows):
            rows.append([])

            for j in range(self.cols):
                if isinstance(other, Matrix):
                    value = other.matrix[i][j]
                else:
                    value = other

                try:
                    v = self.matrix[i][j] + value
                except (ValueError, TypeError):
                    v = value + self.matrix[i][j]

                rows[i].append(v)
        
        return Matrix(*rows)

    def __sub__(self, other: typing.Union[IntegerType, Matrix]) -> Matrix:
        rows = list()

        if isinstance(other, Matrix) and ((other.rows != self.rows) or (other.cols != self.cols)):
            raise ValueError('Provided matrix has not got the same dimensions')

        for i in range(self.rows):
            rows.append([])

            for j in range(self.cols):
                if isinstance(other, Matrix):
                    value = other.matrix[i][j]
                else:
                    value = other

                rows[i].append(
                    self.matrix[i][j] - value
                )
        
        return Matrix(*rows)

    def __mul__(self, other: typing.Union[IntegerType, Matrix]) -> Matrix:
        rows = list()

        if not isinstance(other, Matrix):
            for i in range(self.rows):
                rows.append([])

                for j in range(self.cols):
                    rows[i].append(
                        self.matrix[i][j] * other
                    )
            return Matrix(*rows)

        if self.dimensions[::-1] != other.dimensions:
            raise ValueError(f'Matrix provided does not have the dimensions: {self.dimensions[::-1]}')

        DIMENSIONS = (self.rows, other.cols)

        for i in range(self.rows):
            rowElements = self.get_row(i)
            rows.append([])

            for j in range(other.cols):
                colElements = other.get_column(j)

                prod = 0
                for index, el in enumerate(rowElements):
                    prod += el * colElements[index]
                rows[i].append(prod)

        mt = Matrix(*rows)

        if mt.dimensions != DIMENSIONS:
            raise ValueError(f'Product matrix did not have the correct dimensions. Expected {DIMENSIONS} got {mt.dimensions}') 

        return mt

    def __matmul__(self, other: typing.Union[IntegerType, Matrix]) -> Matrix:
        return self.__mul__(other)

    def __div__(self, other: typing.Union[IntegerType, Matrix]) -> Matrix:
        return self * other.inverse()

    def __repr__(self) -> str:

        if not self.matrix:
            return "Matrix([])"

        reprString = ""

        for row in self.matrix:
            reprString += '\t'
            reprString += ' '.join(map(str, row))
            reprString += '\n'

        reprString = f'Matrix(\n{reprString})'

        return reprString

    def __call__(self, col: int, row: int):
        """ Get a specific element from the matrix, ``Matrix(...)(0, 0)`` yields the first result """
        return self.matrix[col][row]

    def __getitem__(self, key):
        """ Allows you to fetch the matrix elements by index """
        if isinstance(key, slice):
            start = key.start
            end = key.stop
            # step = key.step

            # start -> col
            # end -> row
            if not start and end:
                return self.get_row(end)
            if start and not end:
                return self.get_column(start)

            return self.matrix[start][end]
        
        return self.matrix[key]

    def __setitem__(self, key, value) -> None:
        try:
            from cake import convert_type

            value = convert_type(value)
        except (ValueError, TypeError):
            pass

        if isinstance(key, slice):
            start = key.start
            end = key.stop

            if start and end:
                self.matrix[start][end] = value
            if not start and end:
                self.matrix[0][end] = value
            if start and not end:
                self.matrix[start][0] = value
            if not start and not end:
                self.matrix[0][0] = value
        
        if isinstance(key, int):
            if not type(value) == list:
                raise TypeError('Provided key was not a list object')
            self.matrix[key] = value

        raise IndexError('This item cannot be set on this matrix')         

    @property
    def dimensions(self) -> tuple:
        return (self.cols, self.rows)


def _BC_DET(M: Matrix, *, cache: bool = False) -> typing.Tuple[Matrix, list]:
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
            for j in range(i + 1, rows):
                M.matrix[k][j] -= M.matrix[k][i] * M.matrix[i][k]
    
    if absmin(M.matrix[rows - 1][rows - 1]) <= tol:
        raise ZeroDivisionError(f'Matrix is numerically singular')

    if cache:
        orig.c_dt = (orig, M, p)
    return orig, M, p
