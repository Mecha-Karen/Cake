from __future__ import annotations
import pprint
import typing



class Matrix:
    def __init__(self, *rows):
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

    def __add__(self, other: typing.Union[int, "Matrix"]) -> "Matrix":
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

    def __sub__(self, other: typing.Union[int, "Matrix"]) -> "Matrix":
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

    def transpose(self) -> Matrix:
        """Returns the tranpose of this matrix."""
        data = self.matrix[0]
        ret = [[data[x][y] for x in range(len(data))] for y in range(len(data[0]))]
        return Matrix(ret)

    def __repr__(self) -> str:
        return pprint.saferepr(self.matrix)
