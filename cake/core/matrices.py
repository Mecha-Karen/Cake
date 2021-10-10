class Matrix:
    def __init__(self, passedMatrixData):
        self.passedMatrixData = passedMatrixData

    def __repr__(self):
        # Adjust representation of object to string
        return repr(self.passedMatrixData)

    def __add__(self, other):
        # Modify the addition method to natively add matrices.
        passedMatrixData = []

        # Nested for loop to split and calculate each matrix item
        for j in range(len(self.passedMatrixData)):
            passedMatrixData.append([])
            lengthMatrixData = len(self.passedMatrixData[0])
            for k in range(lengthMatrixData):
                # Addition operation
                passedMatrixData[j].append(
                    self.passedMatrixData[j][k] + other.passedMatrixData[j][k]
                )

        return Matrix(passedMatrixData)

    def __sub__(self, other):
        # Modify the addition method to natively add matrices.
        passedMatrixData = []

        # Nested for loop to split and calculate each matrix item
        for j in range(len(self.passedMatrixData)):
            passedMatrixData.append([])
            lengthMatrixData = len(self.passedMatrixData[0])
            for k in range(lengthMatrixData):
                # Subtraction operation
                passedMatrixData[j].append(
                    self.passedMatrixData[j][k] - other.passedMatrixData[j][k]
                )

        return Matrix(passedMatrixData)
