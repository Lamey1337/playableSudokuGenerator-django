from .Matrix import Matrix, createEmptyMatrix
from collections import defaultdict
from random import choice, shuffle, randint

class Sudoku:
    """
    
    Create's Sudoku 9x9 field from list of numbers.
    If there's no value return's Sudoku object that is ready to scramble.
    
    """

    def __init__(self, value=False):

        def createSudokuField():
            res = createEmptyMatrix(9)
            for i in res.coardinates:
                x, y = i[0], i[1]
                res.data[x][y] = list(range(1,10))
            return res

        def sepIntoBlocks(coards):

            stack = []
            blocks = defaultdict(list)
            parts = defaultdict(list)
            sortedCoardinates = sorted(coards)

            while sortedCoardinates:
                for i in range(3):
                    item = sortedCoardinates[:3]
                    sortedCoardinates = sortedCoardinates[3:]
                    parts[i].extend(item)

            for coards in parts.values():
                while coards:
                    item = coards[:9]
                    coards = coards[9:]
                    stack.append(item)

            for ind, val in enumerate(stack):
                blocks[ind+1].extend(val)

            return blocks

        def encodeValue(value):
            value = [int(i) for i in value]
            res = []
            while value:
                row, value = value[:9], value[9:]
                res.append(row)
            return Matrix(res)



        self.field = createSudokuField() if not value else encodeValue(value)

        self.blocks = sepIntoBlocks(self.field.coardinates)

        self.cRow = defaultdict(list)
        for i in self.field.coardinates: self.cRow[i[0]].append(i)

        self.cCol = defaultdict(list)
        for i in self.field.coardinates: self.cCol[i[1]].append(i)

    def __str__(self):
        return str(self.field)
    
    def scramble(self):
        """
        
        If there's no value: scramble's current Sudoku object
        
        """
        
        test = list(range(1,10))
        for x in self.field.data:
            for y in x:
                if y != test:
                    raise ValueError("Can't scramble already existing Sudoku. Try genSudoku() instead")
        del(test)

        scramble = createEmptyMatrix(9)

        def refreshRow(coard, val):
            res = []

            for i in self.cRow[coard[0]]:
                x, y = i[0], i[1]
                if val in self.field.data[x][y]:
                    self.field.data[x][y].remove(val)
                if len(self.field.data[x][y]) == 1:
                    res.append(((x, y),self.field.data[x][y].pop()))

            return res

        def refreshCol(coard, val):
            res = []

            for i in self.cCol[coard[1]]:
                x, y = i[0], i[1]
                if val in self.field.data[x][y]:
                    self.field.data[x][y].remove(val)
                if len(self.field.data[x][y]) == 1:
                    res.append(((x, y),self.field.data[x][y].pop()))

            return res

        def refreshBlock(coard, val):
            res = []

            for block in self.blocks:
                if coard not in self.blocks[block]: continue

                for i in self.blocks[block]:
                    x,y = i[0], i[1]
                    if val in self.field.data[x][y]:
                        self.field.data[x][y].remove(val)
                    if len(self.field.data[x][y]) == 1:
                        res.append(((x, y),self.field.data[x][y].pop()))
                break

            return res

        def update(coard, val):

            changed = refreshRow(coard, val)
            if changed:
                for i in changed:
                    x, y = i[0][0], i[0][1]
                    scramble.data[x][y] = i[1]
                    update(*i)

            changed = refreshCol(coard, val)
            if changed:
                for i in changed:
                    x, y = i[0][0], i[0][1]
                    scramble.data[x][y] = i[1]
                    update(*i)

            changed = refreshBlock(coard, val)
            if changed:
                for i in changed:
                    x, y = i[0][0], i[0][1]
                    scramble.data[x][y] = i[1]
                    update(*i)

        randCoard = list(self.field.coardinates)
        shuffle(randCoard)

        for i in randCoard:
            x, y = i[0], i[1]
            if not self.field.data[x][y]: continue

            val = choice(self.field.data[x][y])
            self.field.data[x][y].clear()
            scramble.data[x][y] = val

            update((x, y), val)

        self.field = scramble

        return scramble

    def check(self, trace = False):

        """
        
        Return's True If all all rules right Else False
        Trace will print every move
        
        """

        correct = list(range(1, 10))
        res = []
        checks = []

        for x in sorted(self.cRow.keys()):
            for y in self.cRow[x]:
                res.append(self.field.data[y[0]][y[1]])
            check = (sorted(res) == correct)
            checks.append(check)
            if trace: print(f"Row {x}: {check}")
            if not check: return False
            res.clear()

        for x in sorted(self.cCol.keys()):
            for y in self.cCol[x]:
                res.append(self.field.data[y[0]][y[1]])
            check = (sorted(res) == correct)
            checks.append(check)
            if trace: print(f"Col {x}: {check}")
            if not check: return False
            res.clear()

        for x in sorted(self.blocks.keys()):
            for y in self.blocks[x]:
                res.append(self.field.data[y[0]][y[1]])
            check = (sorted(res) == correct)
            checks.append(check)
            if trace: print(f"Block {x}: {check}")
            if not check: return False
            res.clear()

        if trace: print(f"All rules applied: {all(checks)}")

        return True

    def __iter__(self):
        return iter(self.field)

    def puzzle(self, val=5):

        """
        
        Return list with randomly deleted parts (deleted parts as 0)
        
        """

        res = []

        for x in self:
            for y in x:
                res.append("0") if randint(0, val) == 0 else res.append(str(y))
        return res



def genSudoku(trace=False):

    """
    
    Generate's solved Sudoku object with self.check() -> True

    """

    while True:
        sudoku = Sudoku()
        sudoku.scramble()
        if sudoku.check(trace):
            return sudoku




if __name__ == "__main__":

    #gen test
    sudoku = genSudoku(True)
    print(sudoku)

    #puzzle method test
    puzzle = sudoku.puzzle(2)
    print(puzzle)
    print("_".join(puzzle))

    #sudoku from list test
    value = list(range(81))
    sudoku = Sudoku(value)
    print(sudoku)
    
