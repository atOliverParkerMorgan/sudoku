


class Board:
    def __init__(self):
        self.width = 9
        self.height = 9
        self.board = []
        self.SQUARES = {
            0: [1, 1],
            1: [4, 1],
            2: [7, 1],

            3: [1, 4],
            4: [4, 4],
            5: [7, 4],

            6: [1, 7],
            7: [4, 7],
            8: [7, 7],
        }

        self.NEIGHBOURS = [[1, 1], [0, 1], [-1, -1], [0, -1], [-1, 1], [1, 0], [1, -1], [-1, 0]]

    def getBoardSquare(self, index):
        output = []
        square_position = self.SQUARE_CENTER_CORDS[index]
        for cords in self.NEIGHBOURS:
            output.append(self.getBoardElement(cords[0]+square_position[0], cords[1]+square_position[1]))

        return output


    def isSquareValid(self, index):


    def fillBoard(self):
        for x in range(self.width):
            helperList = []
            for y in range(self.height):
                helperList.append(0)
            self.board.append(helperList)

    # 1 2 3 4 5 6 7 8 9 45
    def isRowValid(self, y):
        sumRow = 0
        for x in range(self.width):
            sumRow += self.getBoardElement(x, y)

        return sumRow <= (self.width / 2) * self.width

    def isColValid(self, x):
        sumColumn = 0
        for y in range(self.height):
            sumColumn += self.getBoardElement(x, y)

        return sumColumn <= (self.height / 2) * self.height

    def printBoard(self):
        for row in self.board:
            print(row)

    def getBoardElement(self, x, y):
        return self.board[y][x]

    def setBoardElement(self, x, y, value):
        self.board[y][x] = value
