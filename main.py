from Board import Board

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    board = Board()
    board.fillBoard()
    board.printBoard()
    print(board.isRowValid(0))
    print(board.isColValid(0))


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
