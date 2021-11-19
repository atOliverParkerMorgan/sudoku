from Board import Board

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    board = Board()
    board.fillBoard()
    board.fillSquareRandom(0)
    board.fillSquareRandom(8)
    # board.fillSquareRandom(4)
    # board.fillSquareRandom(8)
    board.printBoard()



# See PyCharm help at https://www.jetbrains.com/help/pycharm/
