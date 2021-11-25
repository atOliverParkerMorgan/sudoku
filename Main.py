import csv

from Board import Board
from Graphics import Graphics


def generateSuDokuBoards(numberOfBoards):
    with open('preGeneratedSudokuBoards.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for _ in range(numberOfBoards):
            board.fillBoard()
            if board.generatePuzzle(5000000):
                print("SUCCESS\n\n")

                output = []
                for line in board.board:
                    for node in line:
                        output.append(node.value)

                writer.writerow(output)


if __name__ == '__main__':
    board = Board()
    board.fillBoard()

    # g = Graphics(board)
    # g.createMenu()

    generateSuDokuBoards(100)
