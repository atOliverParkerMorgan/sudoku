from Board import Board

if __name__ == '__main__':
    board = Board()
    board.fillBoard()

    board.printBoard()
    print(board.backTracking(10))
    board.printBoard()
