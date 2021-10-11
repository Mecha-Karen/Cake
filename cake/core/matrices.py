from __future__ import annotations
from cake.abc import IntegerType
import pprint
import typing


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
        if not rows:
            self.matrix = []
        else:
            if len(rows) == 1 and isinstance(rows[0][0], (list, tuple)):
                rows = rows[0]

            if any(i for i in rows if len(i) < len(rows[0])):
                raise ValueError('Row lengths in matrix not equal')
            self.matrix = rows

        self.cols = len(rows[0])
        self.rows = len(rows)

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
        data = self.matrix
        ret = [[data[x][y] for x in range(len(data))] for y in range(len(data[0]))]

        return Matrix(*ret)

    def __add__(self, other: typing.Union[IntegerType, Matrix]) -> Matrix:
        rows = list()

        if isinstance(other, Matrix) and ((other.rows != self.rows) or (other.cols != self.cols)):
            raise ValueError('Provided matrix has not got the same dimensions')

        for i in range(self.rows):
            rows.append([])

            if isinstance(other, Matrix):
                value = other.matrix[i][j]
            else:
                value = other

            for j in range(self.cols):
                rows[i].append(
                    self.matrix[i][j] + value
                )
        
        return Matrix(*rows)

    def __sub__(self, other: typing.Union[IntegerType, Matrix]) -> Matrix:
        rows = list()

        if isinstance(other, Matrix) and ((other.rows != self.rows) or (other.cols != self.cols)):
            raise ValueError('Provided matrix has not got the same dimensions')

        for i in range(self.rows):
            rows.append([])

            if isinstance(other, Matrix):
                value = other.matrix[i][j]
            else:
                value = other

            for j in range(self.cols):
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

    def __repr__(self) -> str:
        # CSV formatting kinda
        if not self.matrix:
            return "Matrix([])"

        reprString = ""

        for row in self.matrix:
            reprString += '\t'
            reprString += ' '.join(map(str, row))
            reprString += '\n'

        reprString = f'Matrix(\n{reprString})'

        return reprString

    @property
    def dimensions(self) -> tuple:
        return (self.cols, self.rows)
