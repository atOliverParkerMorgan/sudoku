import random
from typing import List
from Node import Node


class Board:
    def __init__(self):
        self.width = 9
        self.height = 9
        self.board: List[List[Node]] = []
        self.SQUARES = {
            0: [1, 1],
            1: [4, 1],
            2: [7, 1],

            3: [1, 4],
            4: [4, 4],
            5: [7, 4],

            6: [1, 7],
            7: [4, 7],
            8: [7, 7],
        }

        self.VALUES_NEEDED_IN_SQUARE = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        self.NEIGHBOURS = [[1, 1], [0, 1], [-1, -1], [0, -1], [-1, 1], [1, 0], [1, -1], [-1, 0]]

    def fillBoard(self):
        squareIndex = 0
        for y in range(self.height):
            helperList = []
            for x in range(self.width):
                helperList.append(Node(x, y, 0, self.VALUES_NEEDED_IN_SQUARE.copy(), squareIndex))
            self.board.append(helperList)
        for i in range(len(self.VALUES_NEEDED_IN_SQUARE)):
            for node in self.getBoardSquare(i):
                node.squareIndex = i

    def updateRow(self, y, value):
        for x in range(self.width):
            if value in self.getBoardNode(x, y).validValues:
                self.getBoardNode(x, y).validValues.remove(value)

    def updateCol(self, x, value):
        for y in range(self.height):
            if value in self.getBoardNode(x, y).validValues:
                self.getBoardNode(x, y).validValues.remove(value)

    def updateSquare(self, index, value):
        for node in self.getBoardSquare(index):
            if value in self.getBoardNode(node.x, node.y).validValues:
                self.getBoardNode(node.x, node.y).validValues.remove(value)

    def updateBoard(self, node, value):
        self.updateCol(node.x, value)
        self.updateRow(node.y, value)
        self.updateSquare(node.squareIndex, value)

    def getBoardSquare(self, index):
        cords = self.SQUARES[index]
        centreNode = self.getBoardNode(cords[0], cords[1])
        output = [centreNode]

        for cords in self.NEIGHBOURS:
            x, y = cords[0] + output[0].x, cords[1] + output[0].y
            output.append(self.getBoardNode(x, y))

        return output

    def printBoard(self):

        for row in self.board:
            line = ""
            for node in row:
                line += str(node)

            print(line)

    def getBoardNode(self, x, y):
        return self.board[y][x]

    def setBoardNodeValue(self, node, value):
        # it is not valid
        if value not in node.validValues:
            return False

        self.updateBoard(node, value)
        self.board[node.y][node.x].value = value

        return True

    def fillSquareRandom(self, index):
        for node in self.getBoardSquare(index):
            if len(node.validValues) == 0:
                # self.resetSquare(index)
                print(f"Failed to generate valid values for square with index: {index}")
                return
            randomValue = node.validValues[random.randint(0, len(node.validValues) - 1)]

            # print(f"X: {node.x}, Y: {node.y}, value: {randomValue}, squareIndex: {node.squareIndex} ")
            self.setBoardNodeValue(node, randomValue)

    def resetSquare(self, index):
        for node in self.getBoardSquare(index):
            node.value = 0
