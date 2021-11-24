from Board import Board
from Graphics import Graphics

if __name__ == '__main__':
    board = Board()
    board.fillBoard()

    # print(board.backTracking(2))


    # board.generatePuzzle()
    g = Graphics(board)
    g.createMenu()
