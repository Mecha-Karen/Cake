from __future__ import annotations
from cake.abc import IntegerType
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
        from cake import convert_type

        if not rows:
            self.matrix = []
        else:
            if len(rows) == 1 and isinstance(rows[0][0], (list, tuple)):
                rows = rows[0]

            if any(i for i in rows if len(i) < len(rows[0])):
                raise ValueError('Row lengths in matrix not equal')

            rows = [list(map(convert_type, row)) for row in rows]

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

    def determinant(self) -> int:
        if (self.dimensions[0] != self.dimensions[1]) or self.dimensions == (1, 1) or not self.matrix:
            raise ValueError(f'Non-square matrixes cannot have a determinant')

        if self.dimensions == (2, 2):
            # ad - bc
            return (self.matrix[0][0] * self.matrix[1][1]) - (self.matrix[0][1] * self.matrix[1][0])

        if self.dimensions == (3, 3):
            # a(ei - fh) - b(di - fg) + c(dh - eg)
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

        # For huge matrixes, it is inefficient to assign all the vars and so on
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
