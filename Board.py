from typing import List
import csv
import random
import math
from Node import Node

class Board:
    def __init__(self, size=9):
        if math.isqrt(size) ** 2 != size:
            raise ValueError("Size must be a perfect square (e.g., 4, 9, 16)")

        self.size = size
        self.box_size = int(math.sqrt(size))
        self.board: List[List[Node]] = []
        self.fillBoard()
        self.getAffectedCells()

    def getAffectedCells(self):
        self.affected_cells_cache = {}
        for x in range(self.size):
            for y in range(self.size):
                affected = set()

                for i in range(self.size):
                    if i != x:
                        affected.add((i, y))
                    if i != y:
                        affected.add((x, i))

                start_x = x - x % self.box_size
                start_y = y - y % self.box_size
                for i in range(self.box_size):
                    for j in range(self.box_size):
                        bx, by = start_x + i, start_y + j
                        if (bx, by) != (x, y):
                            affected.add((bx, by))

                self.affected_cells_cache[(x, y)] = list(affected)

    def saveBoard(self, filename='savedBoard'):
        with open(f'{filename}.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.getValuesDefault())
            writer.writerow(self.getValuesUser())

    def loadBoard(self, filename='savedBoard', index=0):
        try:
            with open(f'{filename}.csv', 'r') as f:
                rows = list(csv.reader(f))
            start = index * 2
            if start + 1 >= len(rows):
                raise IndexError("Puzzle index out of range")

            self.setBoardWithDefaultValues(rows[start])
            self.setBoardWithUserValues(rows[start + 1])
            return True
        except FileNotFoundError:
            print(f"File {filename}.csv not found")
            return False

    def getValuesDefault(self):
        return [node.value if node.user_cannot_change else 0 for row in self.board for node in row]

    def getValuesUser(self):
        return [node.value if not node.user_cannot_change else 0 for row in self.board for node in row]

    def setBoardWithDefaultValues(self, values):
        for y in range(self.size):
            for x in range(self.size):
                index = y * self.size + x
                value = int(values[index]) if index < len(values) and values[index].isdigit() else 0
                if value:
                    self.setValue(x, y, value)
                    self.getBoardNode(x, y).user_cannot_change = True

    def setBoardWithUserValues(self, values):
        for y in range(self.size):
            for x in range(self.size):
                node = self.getBoardNode(x, y)
                index = y * self.size + x
                if not node.user_cannot_change:
                    value = int(values[index]) if index < len(values) and values[index].isdigit() else 0
                    if value:
                        self.setValue(x, y, value)

    def fillBoard(self):
        self.board = [[Node(x, y, 0, self.size) for x in range(self.size)] for y in range(self.size)]

    def resetNodesOnBoardThatUserChanged(self):
        for y in range(self.size):
            for x in range(self.size):
                node = self.getBoardNode(x, y)
                if not node.user_cannot_change:
                    self.setValue(x, y, 0)

    def updateNodeValidValues(self, x, y):
        node = self.getBoardNode(x, y)
        if node.value != 0:
            node.valid_values = []
            return

        valid = set(range(1, self.size + 1))
        for ax, ay in self.affected_cells_cache[(x, y)]:
            val = self.getBoardNode(ax, ay).value
            if val:
                valid.discard(val)

        node.valid_values = list(valid)

    def updateAllNodesValidValues(self):
        for y in range(self.size):
            for x in range(self.size):
                if self.getBoardNode(x, y).value == 0:
                    self.updateNodeValidValues(x, y)

    def isValueValidForNode(self, x, y, value):
        if value == 0:
            return True
        if not 1 <= value <= self.size:
            return False
        current = self.getBoardNode(x, y).value
        if current == value:
            return True
        return all(self.getBoardNode(ax, ay).value != value for ax, ay in self.affected_cells_cache[(x, y)])

    def getInvalidityReasons(self, x, y, value):
        if value == 0:
            return []
        return [(ax, ay) for ax, ay in self.affected_cells_cache[(x, y)] if self.getBoardNode(ax, ay).value == value]

    def getBoardNode(self, x, y):
        return self.board[y][x]

    def setValue(self, x, y, value):
        try:
            value = int(value)
        except (ValueError, TypeError):
            value = 0

        if value and not self.isValueValidForNode(x, y, value):
            return False

        node = self.getBoardNode(x, y)
        old_value = node.value
        node.value = value
        self._update_affected_domains(x, y, old_value, value)
        return True

    def _update_affected_domains(self, x, y, old_value, new_value):
        self.updateNodeValidValues(x, y)
        for ax, ay in self.affected_cells_cache[(x, y)]:
            if self.getBoardNode(ax, ay).value == 0:
                self.updateNodeValidValues(ax, ay)

    def getNodesWithoutValue(self):
        return [self.getBoardNode(x, y)
                for y in range(self.size)
                for x in range(self.size)
                if self.getBoardNode(x, y).value == 0]

    def generatePuzzle(self, difficulty=0.9):
        from Solver import Solver

        self.fillBoard()
        solver = Solver(self, "minimum-remaining-values")
        if not solver.solve():
            return False

        solution = [[self.getBoardNode(x, y).value for x in range(self.size)] for y in range(self.size)]
        positions = [(x, y) for y in range(self.size) for x in range(self.size)]
        random.shuffle(positions)
        cells_to_remove = int(self.size * self.size * difficulty)

        for i, (x, y) in enumerate(positions):
            if i >= cells_to_remove:
                break
            self.setValue(x, y, 0)

        for y in range(self.size):
            for x in range(self.size):
                node = self.getBoardNode(x, y)
                node.user_cannot_change = (node.value != 0)

        return True

    def setToRandomPreGeneratedBoard(self):
        try:
            self.generatePuzzle(difficulty=0.5)
        except Exception as e:
            print(f"Error generating random board: {e}")
            try:
                self.loadBoard(f'puzzles_{self.size}x{self.size}', random.randint(0, 64))
            except Exception:
                self.generatePuzzle(difficulty=0.3)
