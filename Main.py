import csv

from Board import Board
from Graphics import Graphics

if __name__ == '__main__':
    board = Board()
    board.fillBoard()

    with open('preGeneratedSudokuBoards.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        for _ in range(10):
            board.fillBoard()
            board.generatePuzzle()

            output = []
            for line in board.board:
                for node in line:
                    output.append(node.value)

            writer.writerow(output)
