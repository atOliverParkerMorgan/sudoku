import csv

from Board import Board
from Graphics import Graphics


def checkDataSet():
    for i in range(250):
        board = Board()
        board.fillBoard()
        board.setToPreGeneratedBoard(i)

        for line in board.board:
            for node in line:
                if len(board.getInvalidNode(node, node.value)) > 1 and not str(node.value) == "0":
                    print(f"ERROR: {i}")


def generateSuDokuBoards(numberOfBoards):
    with open('preGeneratedSudokuBoards.csv', 'a', newline='', encoding='utf-8') as f:
        with open('preGeneratedSudokuBoards.csv', 'rt') as f2:

            reader = csv.reader(f2, delimiter=',')
            writer = csv.writer(f)

            for _ in range(numberOfBoards):
                board.fillBoard()
                if board.generatePuzzle(10000000):

                    output = board.getValues()

                    if output not in reader:
                        print("\nSUCCESS\n\n")
                        writer.writerow(output)
                    else:
                        print("this board is already preGenerated")


if __name__ == '__main__':
    # checkDataSet()

    board = Board()
    board.fillBoard()

    g = Graphics(board)
    g.createMenu()
