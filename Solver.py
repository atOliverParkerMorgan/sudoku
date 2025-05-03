from Board import Board

class Solver:
    """Simplified Solver for Sudoku using Minimum Remaining Values (MRV) heuristic."""

    def __init__(self, board: Board, strategy="default"):
        self.board = board
        self.strategy = strategy
        self.solution_count = 0
        self.solutions = []
        self.stack = []
        self.finished = False
        self.backtrack = False
        self.board.updateAllNodesValidValues()

    def solver_tick(self):
        if self.finished:
            return True

        # Check if solved
        if not self.board.getNodesWithoutValue():
            self.finished = True
            return True

        if self.backtrack:
            if not self.stack:
                self.finished = True
                return True  # No more options, no solution

            node, valid_values = self.stack.pop()
            self.board.setValue(node.x, node.y, 0)  # Clear value
            print(f"Backtracking from ({node.x}, {node.y})")
        else:
            empty_nodes = self.board.getNodesWithoutValue()
            self.board.updateAllNodesValidValues()

            if self.strategy == "minimum-remaining-values":
                empty_nodes.sort(key=lambda n: len(n.valid_values))

            node = empty_nodes[0]
            valid_values = node.valid_values.copy()

        while valid_values:
            value = valid_values.pop(0)
            if self.board.setValue(node.x, node.y, value):
                self.stack.append((node, valid_values))  # Save remaining values
                self.backtrack = False
                return False  # Continue solving

        # If no valid values worked, trigger backtracking
        self.backtrack = True
        return False

    def solve(self):
        while not self.solver_tick():
            continue
        return not self.board.getNodesWithoutValue()
