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
        """
        Transpose the matrix
        """
        data = self.matrix
        ret = [[data[x][y] for x in range(len(data))] for y in range(len(data[0]))]

        return Matrix(*ret)

    def inverse(self) -> Matrix:
        """
        Get the inverse of the matrix. Uses the Gauss–Jordan elimination method.
        """
        if self.cols != self.rows:
            raise ValueError('Cannot inverse this matrix, rows and cols are not the same length')
        if self.determinant() == 0:
            raise ValueError('Determinant is zero, therefore inverse matrix doesn\'t exist')

        # Swap row 1 with row -1
        rowOne = self.get_row(0)
        lastRow = self.get_row(-1)

        matrixData = list(self.matrix)

        matrixData[0] = lastRow
        matrixData[-1] = rowOne

        # Multiply middle row by the length of cols
        rowIndex = round(self.rows / 2)
        asMtrx = Matrix(self.get_row(rowIndex))
        asMtrx *= self.cols

        matrixData[rowIndex] = asMtrx.matrix[0]

        # Add the middle row to the first row twice
        row = self.get_row(rowIndex)
        asMtrx = Matrix(self.get_row(rowIndex))
        asMtrx += Matrix(row)
        asMtrx += Matrix(row)

        matrixData[rowIndex] = asMtrx.matrix[0]

        return Matrix(*matrixData)

    def determinant(self) -> int:
        if self.dimensions[0] != self.dimensions[1]:
            raise ValueError(f'Non-square matrixes cannot have a determinant')

        if self.dimensions == (2, 2):
            return (self.matrix[0][0] * self.matrix[1][1]) - (self.matrix[0][1] * self.matrix[1][0])
        if self.dimensions == (3, 3):
            a = self.matrix[0][0]
            b = self.matrix[0][1]
            c = self.matrix[0][2]
            d = self.matrix[1][0]
            e = self.matrix[1][1]
            f = self.matrix[1][2]
            g = self.matrix[2][0]
            h = self.matrix[2][1]
            i = self.matrix[2][2]

            return (a * ((e * i) - (f * h))) - (b * ((d * i) - (f * g))) + (c * ((d * h) - (e * g)))

        # For matrixes 4x4 and higher, coming soon
        raise NotImplementedError()

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

    @property
    def dimensions(self) -> tuple:
        return (self.cols, self.rows)
