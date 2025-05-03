from Board import Board

class Solver:
    """Sudoku Solver using CSP heuristics: MRV, LCV, and forward checking."""

    def __init__(self, board: Board, strategy="minimum-remaining-values"):
        self.board = board
        self.strategy = strategy
        self.solution_count = 0
        self.forced_values = set()
        self.solutions = []
        self.stack = []
        self.finished = False
        self.backtrack = False
        self.board.updateAllNodesValidValues()

    def solver_tick(self):
        if self.finished:
            return True

        if not self.board.getNodesWithoutValue():
            self.finished = True
            return True

        if self.backtrack:
            self.backtrack = False
            if self.forced_values:
                while self.forced_values:
                    node = self.forced_values.pop()
                    self.board.setValue(node.x, node.y, 0)

            if not self.stack:
                self.finished = True
                return True

            node, valid_values = self.stack.pop()
            self.board.setValue(node.x, node.y, 0)

        else:
            empty_nodes = self.board.getNodesWithoutValue()
            self.board.updateAllNodesValidValues()

            # Minimum Remaining Values
            if self.strategy == "minimum-remaining-values":
                empty_nodes.sort(key=lambda n: len(n.valid_values))

            node = empty_nodes[0]
            valid_values = node.valid_values.copy()

            # Least Constraining Value
            if self.strategy == "least-constraining-values":
                def lcv_sort(value):
                    impact = 0
                    for peer_x, peer_y in self.board.getRelatedNodes(node.x, node.y):
                        peer = self.board.getBoardNode(peer_x, peer_y)
                        if value in peer.valid_values:
                            impact += 1
                    return impact
                valid_values.sort(key=lcv_sort)

        while valid_values:
            value = valid_values.pop(0)
            if self.board.setValue(node.x, node.y, value):
                self.stack.append((node, valid_values.copy()))

                # Forward checking: propagate forced values
                self.board.updateAllNodesValidValues()
                changes = True
                while changes:
                    changes = False
                    for forced_node in self.board.getNodesWithoutValue():
                        if len(forced_node.valid_values) == 1:
                            if self.board.setValue(forced_node.x, forced_node.y, forced_node.valid_values[0]):
                                self.forced_values.add(forced_node)
                                changes = True

                if any(len(n.valid_values) == 0 for n in self.board.getNodesWithoutValue()):
                    # Invalid state, undo and try next value
                    for node in self.forced_values:
                        self.board.setValue(node.x, node.y, 0)
                    self.board.setValue(node.x, node.y, 0)
                    self.forced_values.clear()
                    continue

                return False

        self.backtrack = True
        return False

    def solve(self):
        while not self.solver_tick():
            continue
        return not self.board.getNodesWithoutValue()
