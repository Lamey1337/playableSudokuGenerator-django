class Matrix:
    """
    
    Create's simple Matrix object from list

    Example:
    value = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    """

    def __init__(self, value):

        def createCoardinates(data):
            coardinates = set()
            dataLen = len(data)

            for x in range(dataLen):
                for y in range(dataLen):
                    coardinates.add((x, y))

            return coardinates

        self.data = value
        self.matLen = len(self.data[0])
        self.coardinates = createCoardinates(self.data)

    def __str__(self):

        longest = 0
        res = ""

        for x in self.data:
            for y in x:
                valLen = len(str(y))
                if valLen > longest: longest = valLen

        formatedData = createEmptyMatrix(self.matLen).data

        for i in self.coardinates:
            x, y = i[0], i[1]

            formatedVal = str(self.data[x][y])
            formatedVal = (" " * (longest - len(formatedVal))) + formatedVal
            formatedData[x][y] = formatedVal

        for i in formatedData:
            res += str(i) + "\n"

        return res

    def __iter__(self):
        return iter(self.data)


def createEmptyMatrix(matLen):
    """
    
    Create's Matrix object filled with None
    
    """

    emptyCol = [None] * matLen
    emptyMatrix = []

    for i in range(matLen):
        emptyMatrix.append(emptyCol.copy())

    return Matrix(emptyMatrix)

if __name__ == "__main__":

    from random import randint

    def randomMatrix():
        matLen = randint(5, 20)
        emptyMat = createEmptyMatrix(matLen)

        for i in emptyMat.coardinates:
            x, y = i[0], i[1]
            emptyMat.data[x][y] = randint(0, 10000)

        return emptyMat

    matrix1 = randomMatrix()

    print(matrix1)

    for i in matrix1: print(i)