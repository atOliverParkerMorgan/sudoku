class Solver:
    def __init__(self, board, solver_type, number_of_solutions=0):
        self.board = board
        self.number_of_solutions = number_of_solutions
        self.solver_type = solver_type

    def solve(self):
        if self.solver_type == "backtracking":
            return self.backtracking_solver()
        elif self.solver_type == "brute_force":
            return self.brute_force_solver()
        else:
            raise ValueError("Invalid solver type. Use 'backtracking' or 'brute_force'.")

    def backtracking_solver_tick(self, last_node_values, current_index, empty_nodes, target_solutions):
        # If we've examined all empty cells, we found a solution
        if current_index >= len(empty_nodes):
            self.number_of_solutions += 1
            # If we found the target number of solutions, return signal to stop
            if target_solutions > 0 and self.number_of_solutions == target_solutions:
                return -1, self.number_of_solutions
            
            return current_index - 1, self.number_of_solutions
        
        node = empty_nodes[current_index]
        x, y = node.x, node.y
        current_value = last_node_values[node]

        found = False   
        # Try values from current_value to 9         
        for value in range(current_value, 10):
            # Here we check the constraints of the Sudoku board
            if self.board.isNodeValid(x, y, value, check_only_if_is_valid=True):
                # If the value is valid, set it on the board
                self.board.setValue(x, y, value)
                last_node_values[node] = value + 1
                found = True
                return current_index + 1, self.number_of_solutions

        if not found:
            self.board.setValue(x, y, 0)
            last_node_values[node] = 1
            current_index -= 1
            if current_index < 0:
                return -1, self.number_of_solutions
            return current_index, self.number_of_solutions

    def backtracking_solver(self):
        empty_nodes = self.board.getNodesWithoutValue()
        if not empty_nodes:
            return 1
        
        last_node_values = {}
        target_solutions = self.number_of_solutions  
        self.number_of_solutions = 0

        for node in empty_nodes:
            last_node_values[node] = 1

        current_index = 0
        while current_index >= 0 and current_index < len(empty_nodes):
            current_index, _ = self.backtracking_solver_tick(
                last_node_values, current_index, empty_nodes, target_solutions
            )

        return self.number_of_solutions
