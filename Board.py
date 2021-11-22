import random
from typing import List
from Node import Node


class Board:
    def __init__(self):
        self.width = 9
        self.height = 9
        self.board: List[List[Node]] = []
        self.numberOfSolutions = 0

    def fillBoard(self):
        squareIndex = 0
        for y in range(self.height):
            helperList = []
            for x in range(self.width):
                helperList.append(Node(x, y, 0))
            self.board.append(helperList)

    def isNodeValid(self, node, value):
        for x in range(self.width):
            if self.getBoardNode(x, node.y).value == value:
                return False

        for y in range(self.height):
            if self.getBoardNode(node.x, y).value == value:
                return False

        startRow = node.x - node.x % 3
        startCol = node.y - node.y % 3

        for x in range(3):
            for y in range(3):
                if self.getBoardNode(x + startRow, y + startCol).value == value:
                    return False

        return True

    def printBoard(self):

        for row in self.board:
            line = ""
            for node in row:
                line += str(node)

            print(line)

    def getBoardNode(self, x, y):
        return self.board[y][x]

    def randomSolution(self, index):
        pass

    def getNodesWithoutValue(self):
        nodesWithoutValue = []
        for y in range(self.height):
            for x in range(self.width):
                if self.getBoardNode(x, y).value == 0:
                    nodesWithoutValue.append(self.getBoardNode(x, y))

        return nodesWithoutValue

    def getAllSolutions(self):
        nodes = self.getNodesWithoutValue()
        removedNodes = [nodes.pop(0)]
        while len(nodes) > 0:
            removedNodes[0].value += 1

            removedNodes.append(nodes.pop(0))

    def backTrackingRecursion(self, nodes, index=0):

        if index == len(nodes):
            return True

        # num from 1 to 9
        x, y = nodes[index].x, nodes[index].y
        for num in range(1, 10):

            if self.isNodeValid(self.getBoardNode(x, y), num):
                self.getBoardNode(x, y).value = num

                if self.backTrackingRecursion(nodes, index + 1):
                    return True

            self.getBoardNode(x, y).value = 0

        return False

    def backTrackingWithoutRecursion(self, limit=1):
        numberOfSolutions = 0
        nodes = self.getNodesWithoutValue()
        startSearch = {0: 1}
        index = 0

        for i in range(self.width * self.height + 1):
            startSearch[i] = 1

        while index >= 0:

            if index == len(nodes):
                numberOfSolutions += 1
                print()
                self.printBoard()
                print()
                index -= 1
                nodes[index].value += 1
                if numberOfSolutions == limit:
                    return numberOfSolutions

            x, y = nodes[index].x, nodes[index].y

            found = False

            for num in range(startSearch[index], 10):

                if self.isNodeValid(nodes[index], num):
                    self.getBoardNode(x, y).value = num

                    startSearch[index] = num + 1
                    found = True
                    index += 1
                    break

            if not found:
                self.getBoardNode(x, y).value = 0
                startSearch[index] = 1
                index -= 1
        return numberOfSolutions

    def backTracking(self, limit=1):
        self.numberOfSolutions = 0
        return self.backTrackingWithoutRecursion(limit)
        return self.backTrackingRecursion(self.getNodesWithoutValue())
