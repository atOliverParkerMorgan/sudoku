from Board import Board
from Graphics import Graphics
from Solver import Solver

if __name__ == '__main__':
    Graphics(Board(16)).createMenu()
    b = Board(16)
    b.generatePuzzle()
    s = Solver(b)
    s.backtracking_solver()
    b.printBoard()