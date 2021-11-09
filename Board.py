class Board:
    def __init__(self):
        self.width = 9
        self.height = 9
        self.board = [[]]

    def fillBoard(self):
        for x in range(self.width):
            for y in range(self.height):
                self.board[x][y] = 0

    # 1 2 3 4 5 6 7 8 9 45
    def isRowValid(self, y):
        sum = 0
        for x in range(self.width):
            sum += self.board[x][y]

        return sum <= (self.width / 2) * self.width
