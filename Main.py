from Board import Board

if __name__ == '__main__':
    board = Board()
    board.fillBoard()
    board.fillSquareRandom(0)
    board.fillSquareRandom(1)
    board.fillSquareRandom(4)
    board.fillSquareRandom(8)
    # board.fillSquareRandom(8)
    board.printBoard()
