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
                helperList.append(Node(x, y, 0))
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

    def isNodeValid(self, node_x, node_y, value, check_only_if_is_valid=False):
        output = []

        # check horizontally for the same value
        for x in range(self.size):
            if str(self.getBoardNode(x, node_y).value) == str(value) and x != node_x:
                if check_only_if_is_valid:
                    return False
                output.append((x, node_y))

        # check vertically for the same value
        for y in range(self.size):
            if str(self.getBoardNode(node_x, y).value) == str(value) and y != node_y:
                if (node_x, y) not in output:
                    if check_only_if_is_valid:
                        return False
                    output.append((node_x, y))

        # check squares
        # Calculate square size (e.g., for 9x9 board, box_size = 3)
        box_size = int(self.size ** 0.5)
        
        # base square index => startRow, startCol
        startRow = node_x - node_x % box_size
        startCol = node_y - node_y % box_size

        for x in range(box_size):
            for y in range(box_size):
                if str(self.getBoardNode(x + startRow, y + startCol).value) == str(value) and (x + startRow, y + startCol) != (node_x, node_y):
                    if (x + startRow, y + startCol) not in output:
                        output.append((x + startRow, y + startCol))
                        if check_only_if_is_valid:
                            return False

        if check_only_if_is_valid:
            return True
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
        self.getBoardNode(x, y).value = value

    def getNodesWithoutValue(self):
        # get all nodes that have value zero
        nodesWithoutValue = []
        for y in range(self.size):
            for x in range(self.size):
                if str(self.getBoardNode(x, y).value) == "0":
                    nodesWithoutValue.append(self.getBoardNode(x, y))
        return nodesWithoutValue


    def generatePuzzle(self, target_solutions=1, maxSearchDepth=10_000):

        nodes = self.getNodesWithoutValue()
        solver = Solver(self, "backtracking")

        while nodes:
            node = random.choice(nodes)
            x, y = node.x, node.y

            valid_numbers = [num for num in range(1, self.size + 1)
                            if self.isNodeValid(x, y, num, check_only_if_is_valid=True)]

            if not valid_numbers:
                nodes.remove(node)
                continue

            self.setValue(x, y, random.choice(valid_numbers))

            if solver.backtracking_solver(target_solutions, maxSearchDepth) == 0:
                self.setValue(x, y, 0)  # Undo placement if it leads to no solution
            else:
                nodes.remove(node)  # Keep the value and move on

        for y in range(self.size):
            for x in range(self.size):
                node = self.getBoardNode(x, y)
                if random.random() <= 0.85:
                    self.setValue(x, y, 0)
                else:
                    node.user_cannot_change = True

        return True
