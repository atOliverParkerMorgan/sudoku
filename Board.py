import random
from typing import List
from Node import Node


class Board:
    def __init__(self):
        # sudoku 9x9
        self.width = 9
        self.height = 9

        # 2d board with all sudoku Nodes
        self.board: List[List[Node]] = []

    def fillBoard(self):
        # reset board
        self.board: List[List[Node]] = []

        # create new board with nodes that have value zero
        for y in range(self.height):
            helperList = []
            for x in range(self.width):
                helperList.append(Node(x, y, 0))
            self.board.append(helperList)

    def resetNodesOnBoard(self, nodes):
        # reset all node value to zero
        for node in nodes:
            self.setValue(node.x, node.y, 0)
            self.getBoardNode(node.x, node.y).userCannotChange = False

    def isNodeValid(self, node, value):
        # check horizontally for the same value
        for x in range(self.width):
            if self.getBoardNode(x, node.y).value == value:
                return False

        # check vertically for the same value
        for y in range(self.height):
            if self.getBoardNode(node.x, y).value == value:
                return False

        # check squares
        # base square index => startRow, startCol
        startRow = node.x - node.x % 3
        startCol = node.y - node.y % 3

        for x in range(3):
            for y in range(3):
                if self.getBoardNode(x + startRow, y + startCol).value == value:
                    return False

        return True

    def tryToSetValueOfNode(self, x, y, value):
        if self.isNodeValid(self.getBoardNode(x, y), 1):
            self.setValue(x, y, value)

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

    def randomSolution(self, index):
        pass

    def getNodesWithoutValue(self):
        # get all nodes that have value zero

        nodesWithoutValue = []
        for y in range(self.height):
            for x in range(self.width):
                if self.getBoardNode(x, y).value == 0:
                    nodesWithoutValue.append(self.getBoardNode(x, y))

        return nodesWithoutValue

    def backTrackingRecursion(self, nodes, index=0):
        """
        :param nodes: all nodes that must be solved
        :param index: the current index of node that is being solved
        :return: True if a solution as been found else False
        """

        if index == len(nodes):
            # a valid solution to the board has been found
            return True

        x, y = nodes[index].x, nodes[index].y

        # check nodes from 1-9
        for num in range(1, 10):

            if self.isNodeValid(self.getBoardNode(x, y), num):
                # set node to valid value
                self.getBoardNode(x, y).value = num

                # check if next node (node[index + 1]) is valid
                if self.backTrackingRecursion(nodes, index + 1):
                    return True

            # num is not a valid value => reset
            self.getBoardNode(x, y).value = 0

        # no valid value for this board combination
        return False

    def backTrackingWithoutRecursion(self, limit=1, saveSolution=True, maxNumberOfLoops=-1):
        """
        :param limit: a limit of solution to search for
        :param saveSolution: if True save the last solution to the self.board
        :param maxNumberOfLoops: number of loops the algorithm is allowed to go through. -1 if infinite
        :return: number of solution found; -1 if the algorithm exceeds the maxNumberOfLoops
        """
        numberOfLoops = 0

        numberOfSolutions = 0
        nodes = self.getNodesWithoutValue()

        # :startSearch: key => index of node; value => last valid value of node
        # used to know from where to start searching for valid value
        startSearch = {}

        # currentIndex
        index = 0

        # save nodes to copy to reset later
        nodesCopy = nodes.copy()

        # initialize startSearch
        for i in range(self.width * self.height + 1):
            startSearch[i] = 1

        while index >= 0:

            if maxNumberOfLoops != -1:
                numberOfLoops += 1
                if numberOfLoops >= maxNumberOfLoops:
                    return -1

            # the algorithm has found a solution, because index is past the last node
            if index == len(nodes):
                numberOfSolutions += 1

                if numberOfSolutions == limit:

                    # reset board
                    if not saveSolution:
                        self.resetNodesOnBoard(nodesCopy)

                    return numberOfSolutions

                # print the current state of the board
                # print()
                # self.printBoard()
                # print()

                # limit has not yet been reached
                # move to last node
                index -= 1
                # make last node invalid so that the algorithm has to find another combination that is valid
                nodes[index].value += 1

            x, y = nodes[index].x, nodes[index].y

            # does this node have valid value
            found = False

            for num in range(startSearch[index], 10):

                if self.isNodeValid(nodes[index], num):
                    self.getBoardNode(x, y).value = num

                    # set start node begging value for future searches
                    startSearch[index] = num + 1
                    found = True

                    # check next node
                    index += 1

                    break

            if not found:
                # reset not because it has no valid value
                self.getBoardNode(x, y).value = 0
                startSearch[index] = 1

                # move to previous node
                index -= 1

        if not saveSolution:
            self.resetNodesOnBoard(nodesCopy)

        return numberOfSolutions

    def backTracking(self, limit=1):
        return self.backTrackingWithoutRecursion(limit)
        # return self.backTrackingRecursion(self.getNodesWithoutValue())

    def generatePuzzle(self):
        nodes = self.getNodesWithoutValue()

        while nodes:

            # get random node
            randomIndex = random.randint(0, len(nodes) - 1)
            x, y = nodes[randomIndex].x, nodes[randomIndex].y

            # get all valid values for this node
            validNumList = [num for num in range(1, 10) if self.isNodeValid(nodes[randomIndex], num)]

            # set the node to a random value for all valid values
            self.setValue(x, y, validNumList[random.randint(0, len(validNumList) - 1)])

            # if the board doesn't have a solution, because of the new value => reset
            numberOfSolutions = self.backTrackingWithoutRecursion(1, False, 1000000)

            # returns -1 if the algorithm searches through 10 000 000 loops without result
            # this puzzle is too costly to generate
            if numberOfSolutions == -1:
                print("\n\n\n ATTENTION: Search has been restarted current search is too costly \n\n\n")
                return

            # return 0 if the puzzle has no solution
            if numberOfSolutions == 0:
                self.setValue(x, y, 0)

            else:
                # the node has been successfully generated
                nodes.pop(randomIndex)

            print(f"Loading: {81 - len(nodes)} %")

        # a valid random board has been generated

        # add all nodes cords to a list
        allNodesList = []
        for x in range(self.width):
            for y in range(self.height):
                allNodesList.append((x, y))

        # shuffle allNodesList randomly
        randomNodeList = []
        while allNodesList:
            randomNodeList.append(allNodesList.pop(random.randint(0, len(allNodesList) - 1)))

        # try to remove as many nodes as possible while maintaining the puzzle uniqueness
        # (the puzzle has to have only one solution)
        while randomNodeList:
            x, y = randomNodeList.pop(0)

            # save node valuxe in case the uniqueness of the puzzle breaks down once this node is removed
            value = self.getBoardNode(x, y).value

            # remove node value
            self.setValue(x, y, 0)

            # if the puzzle has two solution => set the node to its original value
            print(f"Loading: {81 + len(randomNodeList)} %")
            if self.backTrackingWithoutRecursion(2, False) == 2:
                self.setValue(x, y, value)

                # user cannot change this node its apart of the puzzle
                self.getBoardNode(x, y).userCannotChange = True
