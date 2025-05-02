import csv
import random
from typing import List
from Node import Node
import math
from Solver import Solver

class Board:
    def __init__(self, size=9):
        # sudoku with size x size dimensions (default 9x9)
        if math.isqrt(size) ** 2 != size:
            raise ValueError("Size must be a perfect square (e.g., 4, 9, 16, etc.)")
        self.size = size

        # 2d board with all sudoku Nodes
        self.board: List[List[Node]] = []
        
        # Initialize empty board
        self.fillBoard()


    def saveBoard(self, filename='saved'):
        with open(f'{filename}_{self.size}x{self.size}.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.getValuesDefault())
            writer.writerow(self.getValuesUser())


    def loadBoard(self, filename='saved', index=0):
        with open(f'{filename}.csv', 'rt', encoding='utf-8') as f:
            reader = list(csv.reader(f))

            # Each puzzle uses 2 rows (default and user values)
            start = index * 2
            end = start + 2

            if end > len(reader):
                raise IndexError("Puzzle index out of range.")

            self.setBoardWithDefaultValues(reader[start])
            self.setBoardWithUserValues(reader[start + 1])


    def getValuesDefault(self):
        output = []
        for line in self.board:
            for node in line:
                if node.user_cannot_change:
                    output.append(node.value)
                else:
                    output.append(0)
        return output

    def getValuesUser(self):
        output = []
        for line in self.board:
            for node in line:
                if not node.user_cannot_change:
                    output.append(node.value)
                else:
                    output.append(0)
        return output

    def getValues(self):
        output = []
        for line in self.board:
            for node in line:
                output.append(node.value)
        return output

    def setBoardWithDefaultValues(self, values):
        # set all node value to a newly chosen value
        index = 0
        for y in range(self.size):
            for x in range(self.size):
                self.setValue(x, y, values[index])
                self.getBoardNode(x, y).user_cannot_change = str(values[index]) != "0"
                index += 1

    def setBoardWithUserValues(self, values):
        # set all node value to a newly chosen value
        index = 0
        for y in range(self.size):
            for x in range(self.size):
                if not self.getBoardNode(x, y).user_cannot_change:
                    self.setValue(x, y, values[index])
                index += 1

    def fillBoard(self):
        # reset board
        self.board: List[List[Node]] = []

        # create new board with nodes that have value zero
        for y in range(self.size):
            helperList = []
            for x in range(self.size):
                helperList.append(Node(x, y, 0, self.size))
            self.board.append(helperList)

    def resetNodesOnBoard(self, nodes):
        # reset all node value to zero
        for node in nodes:
            self.setValue(node.x, node.y, 0)
            self.getBoardNode(node.x, node.y).user_cannot_change = False

    def resetNodesOnBoardThatUserChanged(self):
        # reset all node value to zero that user changed
        for x in range(self.size):
            for y in range(self.size):
                node = self.getBoardNode(x, y)
                if not node.user_cannot_change:
                    self.setValue(node.x, node.y, 0)

    def updateNodeValidValues(self, node_x, node_y):
        # Get the node we're updating
        node = self.getBoardNode(node_x, node_y)
        
        # Start with all values as valid, except the node's own value if it's set
        node.valid_values = [i for i in range(1, self.size + 1)]
        if node.value != 0:
            if node.value in node.valid_values:
                node.valid_values.remove(node.value)
        
        # Check row constraints
        for x in range(self.size):
            if x != node_x:  # Skip the current node
                value = self.getBoardNode(x, node_y).value
                if value != 0 and value in node.valid_values:
                    node.valid_values.remove(value)
        
        # Check column constraints
        for y in range(self.size):
            if y != node_y:  # Skip the current node
                value = self.getBoardNode(node_x, y).value
                if value != 0 and value in node.valid_values:
                    node.valid_values.remove(value)
        
        # Check box constraints
        box_size = int(self.size ** 0.5)
        startRow = node_x - node_x % box_size
        startCol = node_y - node_y % box_size
        
        for x in range(box_size):
            for y in range(box_size):
                if (startRow + x, startCol + y) != (node_x, node_y):  # Skip the current node
                    value = self.getBoardNode(startRow + x, startCol + y).value
                    if value != 0 and value in node.valid_values:
                        node.valid_values.remove(value)

    def isValueValidForNode(self, node_x, node_y, value):
        # Check if value is already present in this node
        node = self.getBoardNode(node_x, node_y)
        if str(node.value) != "0" and str(node.value) == str(value):
            return True
            
        # Check if the value is allowed
        if str(value) not in [str(i) for i in range(1, self.size + 1)]:
            return False
            
        # Check for conflicts in row, column, and box
        conflicts = self.getInvalidityReasons(node_x, node_y, value)
        return len(conflicts) == 0

    def getInvalidityReasons(self, node_x, node_y, value, check_only_if_is_valid=False):
        """Returns a list of coordinates where the value conflicts with the given position"""
        output = []
        
        # Skip checks if value is 0 (empty)
        if str(value) == "0":
            return output

        # Check row conflicts
        for x in range(self.size):
            if x != node_x and str(self.getBoardNode(x, node_y).value) == str(value):
                output.append((x, node_y))
                if check_only_if_is_valid:
                    return []  # Early exit if we only need to check validity

        # Check column conflicts
        for y in range(self.size):
            if y != node_y and str(self.getBoardNode(node_x, y).value) == str(value):
                if (node_x, y) not in output:  # Avoid duplicates
                    output.append((node_x, y))
                    if check_only_if_is_valid:
                        return []

        # Check box conflicts
        box_size = int(self.size ** 0.5)
        startRow = node_x - node_x % box_size
        startCol = node_y - node_y % box_size

        for x in range(box_size):
            for y in range(box_size):
                rx, ry = x + startRow, y + startCol
                if (rx, ry) != (node_x, node_y) and str(self.getBoardNode(rx, ry).value) == str(value):
                    if (rx, ry) not in output:  # Avoid duplicates
                        output.append((rx, ry))
                        if check_only_if_is_valid:
                            return []

        # If check_only_if_is_valid is True, an empty list means it's invalid
        # Otherwise, we return all conflicts
        if check_only_if_is_valid:
            return [True]  # No conflicts found, so it's valid
            
        return output

    def printBoard(self):
        for row in self.board:
            line = ""
            for node in row:
                line += str(node)
            print(line)

    def getBoardNode(self, x, y):
        return self.board[y][x]

    def setValue(self, x, y, value):
        # Convert value to int if it's a string
        if isinstance(value, str) and value.isdigit():
            value = int(value)
        elif isinstance(value, str) and value == '':
            value = 0
            
        # If it's still not an int, make it 0
        if not isinstance(value, int):
            value = 0
        
        # Check if value is valid
        if value != 0 and not self.isValueValidForNode(x, y, value):
            self.getBoardNode(x, y).value = 0
            return False

        # Set the value
        self.getBoardNode(x, y).value = value
        
        # Update valid values for this node and affected nodes
        self.updateValidValuesForAllAffectedNodes(x, y)
        return True
    
    def updateValidValuesForAllAffectedNodes(self, x, y):
        """Updates valid values for the node at (x,y) and all nodes in the same row, column, and box"""
        # Update the node itself
        self.updateNodeValidValues(x, y)
        
        # Update nodes in the same row
        for i in range(self.size):
            if i != x:
                self.updateNodeValidValues(i, y)
                
        # Update nodes in the same column
        for i in range(self.size):
            if i != y:
                self.updateNodeValidValues(x, i)
                
        # Update nodes in the same box
        box_size = int(self.size ** 0.5)
        startRow = x - x % box_size
        startCol = y - y % box_size
        
        for i in range(box_size):
            for j in range(box_size):
                if (startRow + i, startCol + j) != (x, y):
                    self.updateNodeValidValues(startRow + i, startCol + j)

    def getNodesWithoutValue(self):
        # get all nodes that have value zero
        nodesWithoutValue = []
        for y in range(self.size):
            for x in range(self.size):
                node = self.getBoardNode(x, y)
                if str(node.value) == "0":
                    nodesWithoutValue.append(self.getBoardNode(x, y))
        return nodesWithoutValue


    def generatePuzzle(self, target_solutions=1, maxSearchDepth=10_000):
        solver = Solver(self)
        solver.backtracking_solver(target_solutions, maxSearchDepth)

        for y in range(self.size):
            for x in range(self.size):
                node = self.getBoardNode(x, y)
                if random.random() <= 0.85:
                    self.setValue(x, y, 0)
                else:
                    node.user_cannot_change = True

        return True