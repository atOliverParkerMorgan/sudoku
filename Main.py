from Board import Board

if __name__ == '__main__':
    board = Board()
    board.fillBoard()

    print(board.backTracking(20))


