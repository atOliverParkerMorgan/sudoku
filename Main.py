from Board import Board
from Graphics import Graphics
from Solver import Solver

if __name__ == '__main__':
    Graphics(Board(16)).createMenu()
    print("Welcome to Sudoku Solver!")
    b = Board(9)
    b.generatePuzzle()
    s = Solver(b)
    s.solve()
    print("Solved Sudoku:")
    b.printBoard()