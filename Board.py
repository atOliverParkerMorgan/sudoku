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

    def getBoardSquare(self, index):
        cords = self.SQUARES[index]
        centreNode = self.getBoardNode(cords[0], cords[1])
        output = [centreNode]

        for cords in self.NEIGHBOURS:
            x, y = cords[0] + output[0].x, cords[1] + output[0].y
            output.append(self.getBoardNode(x, y))

        return output

    def isSquareValid(self, index):
        numbersInSquare = self.VALUES_NEEDED_IN_SQUARE
        for node in self.getBoardSquare(index):
            if node.value in numbersInSquare:
                numbersInSquare.remove(node.value)
            else:
                return False

        return True

    def updateSquare(self, index, value):
        for node in self.getBoardSquare(index):
            if value in node.validValues:
                node.validValues.remove(value)

    def fillBoard(self):
        for x in range(self.width):
            helperList = []
            for y in range(self.height):
                squareIndex = 0
                maxX = 2
                maxY = 2
                while x > maxX and y > maxY:
                    squareIndex += 1
                    if maxY == self.height - 1:
                        maxY = 2
                        maxX += 3
                    else:
                        maxY += 3

                helperList.append(Node(x, y, 0, self.VALUES_NEEDED_IN_SQUARE.copy(), squareIndex))
            self.board.append(helperList)

    def isRowValid(self, y):
        for x in range(self.width):
            if len(self.getBoardNode(x, y).validValues) > 0:
                return False

        return True

    def updateRow(self, y, value):
        for x in range(self.width):
            if value in self.getBoardNode(x, y).validValues:
                self.getBoardNode(x, y).validValues.remove(value)

    def isColValid(self, x):
        for y in range(self.height):
            if len(self.getBoardNode(x, y).validValues) > 0:
                return False

        return True

    def updateCol(self, x, value):
        for y in range(self.height):
            print(value)
            print(self.getBoardNode(x, y).validValues)

            self.getBoardNode(x, y).validValues.remove(value)


    def updateBoard(self, node, value):
        self.updateCol(node.x, value)
        self.updateRow(node.y, value)
        self.updateSquare(node.squareIndex, value)

    def printBoard(self):

        for row in self.board:
            line = ""
            for node in row:
                line += str(node)

            print(line)

    def getBoardNode(self, x, y):
        return self.board[y][x]

    def setBoardNodeValue(self, node, value):
        if self.board[node.y][node.x].value == 0:
            self.updateBoard(node, value)

        self.board[node.y][node.x].value = value

    def fillSquareRandom(self, index):
        for node in self.getBoardSquare(index):

            randomValue = node.validValues[random.randint(0, len(node.validValues) - 1)]
            print(f"X: {node.x}, Y: {node.y}, value: {randomValue} ")
            self.setBoardNodeValue(node, randomValue)
