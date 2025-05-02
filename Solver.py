class Solver:
    def __init__(self, board, heuristic="minimum-remaining-values"):
        self.board = board
        self.number_of_solutions = 0
        self.backtracking_nodes = []
        self.heuristic = heuristic
        if heuristic != "minimum-remaining-values" and heuristic != "least-constraining-values":
            raise ValueError("Heuristic must be 'minimum-remaining-values' or 'least-constraining-values'")

    def backtracking_solver(self, target_solutions=1, maxSearchDepth=-1):
        """
        Solve the Sudoku board using backtracking with the selected heuristic.
        
        Args:
            target_solutions: Number of solutions to find before stopping (default: 1)
            maxSearchDepth: Maximum number of search steps (default: -1, unlimited)
            
        Returns:
            Number of solutions found
        """
        # Reset solution counter
        self.number_of_solutions = 0
        self.backtracking_nodes = []
        
        # Apply forward checking first
        self.apply_forward_checking()
        
        # Start solving
        search_steps = 0
        search_complete = False
        
        while not search_complete:
            # If we have reached the maximum search depth, stop
            if maxSearchDepth > 0 and search_steps >= maxSearchDepth:
                break
                
            # Perform one step of backtracking
            search_complete = self.backtracking_solver_tick(target_solutions)
            search_steps += 1
            
            # If we've reached the search depth limit, stop
            if maxSearchDepth > 0 and search_steps >= maxSearchDepth:
                break
        
        return self.number_of_solutions

    def apply_forward_checking(self):
        """Apply forward checking to fill cells with only one valid value."""
        forward_check_done = False
        
        while not forward_check_done:
            forward_check_done = True
            empty_nodes = self.board.getNodesWithoutValue()
            
            for node in empty_nodes:
                # Update valid values for this node
                self.board.updateNodeValidValues(node.x, node.y)
                
                # If there's only one valid value, set it
                if len(node.valid_values) == 1:
                    value = node.valid_values[0]
                    if self.board.setValue(node.x, node.y, value):
                        forward_check_done = False
                        break
                        
                # If there are no valid values, the board is unsolvable
                elif len(node.valid_values) == 0:
                    return False
        
        return True

    def backtracking_solver_tick(self, target_solutions=1):
        """
        Perform one step of backtracking solving algorithm.
        
        Args:
            target_solutions: Number of solutions to find before stopping
            
        Returns:
            True if the search has ended (found solution or no more possibilities),
            False if search should continue
        """
        empty_nodes = self.board.getNodesWithoutValue()
        
        # If board is solved, increment solution count
        if len(empty_nodes) == 0:
            self.number_of_solutions += 1
            self.backtracking_nodes = []
            # Search ends if we've found enough solutions
            return target_solutions > 0 and self.number_of_solutions >= target_solutions
        
        # Select the next node to fill based on heuristic
        node = self.select_next_node(empty_nodes)
        
        if node is None:
            # If we can't find a new node but have backtracking nodes, use one of those
            if len(self.backtracking_nodes) > 0:
                node = self.backtracking_nodes.pop()
            else:
                # No more nodes to try, we're done
                return True
        
        # Get the values to try based on the heuristic
        values_to_try = self.get_values_to_try(node, empty_nodes)
        
        # Try each value
        value_found = False
        for value in values_to_try:
            # Try to set the value
            if self.board.setValue(node.x, node.y, value):
                value_found = True
                break
        
        if value_found:
            # If we found a valid value, don't add to backtracking yet
            # Just continue the search
            return False
        else:
            # If we get here, no valid value was found
            # Reset the node and add it to backtracking
            self.board.setValue(node.x, node.y, 0)
            if node not in self.backtracking_nodes:
                self.backtracking_nodes.append(node)
            
            # If we've exhausted all possibilities, return True
            if len(self.backtracking_nodes) == 0:
                return True
            
            return False

    def select_next_node(self, empty_nodes):
        """
        Select the next node to fill based on the current heuristic.
        
        Args:
            empty_nodes: List of empty nodes
            
        Returns:
            The next node to fill, or None if no suitable node is found
        """
        if self.heuristic == "minimum-remaining-values":
            return self.select_mrv_node(empty_nodes)
        else:  # least-constraining-values
            if empty_nodes:
                # For LCV we just pick the first empty node since LCV is about value ordering
                return empty_nodes[0]
            return None
    
    def select_mrv_node(self, empty_nodes):
        """
        Select the node with the minimum remaining values.
        
        Args:
            empty_nodes: List of empty nodes
            
        Returns:
            Node with the minimum remaining values, or None if no suitable node is found
        """
        if not empty_nodes:
            return None
            
        # Update valid values for all nodes
        for node in empty_nodes:
            self.board.updateNodeValidValues(node.x, node.y)
        
        # Find the node with the fewest valid values
        min_node = None
        min_val = float('inf')
        
        for node in empty_nodes:
            # Skip nodes we're already backtracking from
            if node in self.backtracking_nodes:
                continue
                
            num_values = len(node.valid_values)
            if num_values < min_val and num_values > 0:
                min_val = num_values
                min_node = node
        
        return min_node

    def get_values_to_try(self, node, empty_nodes):
        """
        Get the values to try for the given node based on the current heuristic.
        
        Args:
            node: The node to find values for
            empty_nodes: All empty nodes
            
        Returns:
            List of values to try
        """
        # Update valid values for this node
        self.board.updateNodeValidValues(node.x, node.y)
        
        if self.heuristic == "least-constraining-values":
            return self.get_least_constraining_values(node, empty_nodes)
        else:
            # For MRV, just use the valid values in any order
            return node.valid_values

    def get_least_constraining_values(self, node, empty_nodes):
        """
        Sort values for a node from least to most constraining.
        
        Args:
            node: The node to find values for
            empty_nodes: All empty nodes
            
        Returns:
            List of values sorted by how little they constrain other nodes
        """
        # For each possible value, calculate how many options it eliminates from other nodes
        constraints = {}
        
        for value in node.valid_values:
            # Save current state of all nodes
            original_values = {}
            for n in empty_nodes:
                if n != node:
                    self.board.updateNodeValidValues(n.x, n.y)
                    original_values[n] = set(n.valid_values)
            
            # Try setting the value
            original_value = node.value
            self.board.setValue(node.x, node.y, value)
            
            # Calculate constraints (how many values are eliminated from other nodes)
            constraint_count = 0
            for n in empty_nodes:
                if n != node:
                    # Update valid values
                    self.board.updateNodeValidValues(n.x, n.y)
                    # Count eliminated values
                    if hasattr(n, 'valid_values'):
                        constraint_count += len(original_values[n]) - len(set(n.valid_values))
            
            constraints[value] = constraint_count
            
            # Reset the board
            self.board.setValue(node.x, node.y, original_value)
            
            # Restore original valid_values for all affected nodes
            for n in empty_nodes:
                if n != node:
                    self.board.updateNodeValidValues(n.x, n.y)
        
        # Sort values by increasing constraint count
        return sorted(node.valid_values, key=lambda v: constraints.get(v, float('inf')))