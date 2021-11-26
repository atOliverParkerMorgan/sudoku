import csv

from Board import Board
from Graphics import Graphics


def generateSuDokuBoards(numberOfBoards):
    with open('preGeneratedSudokuBoards.csv', 'a', newline='', encoding='utf-8') as f:
        with open('preGeneratedSudokuBoards.csv', 'rt') as f2:

            reader = csv.reader(f2, delimiter=',')  # good point by @paco
            writer = csv.writer(f)

            for _ in range(numberOfBoards):
                board.fillBoard()
                if board.generatePuzzle(10000000):

                    output = []
                    for line in board.board:
                        for node in line:
                            output.append(node.value)

                    if output not in reader:
                        print("\nSUCCESS\n\n")
                        writer.writerow(output)
                    else:
                        print("this board is already preGenerated")


if __name__ == '__main__':
    board = Board()
    board.fillBoard()

    g = Graphics(board)
    g.createMenu()

    generateSuDokuBoards(1000000000000)
