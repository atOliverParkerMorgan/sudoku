import csv
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
        self.row_possible_values = [i for i in range(1, 10)]
        self.col_possible_values = [i for i in range(1, 10)]
        self.square_possible_values = [i for i in range(1, 10)]


    def saveBoard(self):
        open('savedBoard.csv', 'w').close()
        with open('savedBoard.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(self.getValuesDefault())
            writer.writerow(self.getValuesUser())

    def loadBoard(self):
        with open('savedBoard.csv', 'rt') as f:
            reader = list(csv.reader(f, delimiter=','))
            self.setBoardWithDefaultValues(reader[0])
            self.setBoardWithUserValues(reader[1])

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
        for y in range(self.height):
            for x in range(self.width):
                self.setValue(x, y, values[index])
                self.getBoardNode(x, y).user_cannot_change = str(values[index]) != "0"
                index += 1

    def setBoardWithUserValues(self, values):
        # set all node value to a newly chosen value
        index = 0
        for y in range(self.height):
            for x in range(self.width):
                if not self.getBoardNode(x, y).user_cannot_change:
                    self.setValue(x, y, values[index])

                index += 1

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

    def resetNodesOnBoardThatUserChanged(self):
        # reset all node value to zero that user changed
        for x in range(self.width):
            for y in range(self.height):
                node = self.getBoardNode(x, y)
                if not node.user_cannot_change:
                    self.setValue(node.x, node.y, 0)


    def isNodeValid(self, node_x, node_y, value, check_only_if_is_valid=False):
        output = []

        # check horizontally for the same value
        for x in range(self.width):
            if str(self.getBoardNode(x, node_y).value) == str(value):
                if check_only_if_is_valid:
                    return False
                output.append((x, node_y))

        # check vertically for the same value
        for y in range(self.height):
            if str(self.getBoardNode(node_x, y).value) == str(value):
                if (node_x, y) not in output:
                    if check_only_if_is_valid:
                        return False
                    output.append((node_x, y))

        # check squares
        # base square index => startRow, startCol
        startRow = node_x - node_x % 3
        startCol = node_y - node_y % 3

        for x in range(3):
            for y in range(3):
                if str(self.getBoardNode(x + startRow, y + startCol).value) == str(value):
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
        self
        self.getBoardNode(x, y).value = value

    def randomSolution(self, index):
        pass

    def getNodesWithoutValue(self):
        # get all nodes that have value zero

        nodesWithoutValue = []
        for y in range(self.height):
            for x in range(self.width):
                if str(self.getBoardNode(x, y).value) == "0":
                    nodesWithoutValue.append(self.getBoardNode(x, y))

        return nodesWithoutValue



    def generatePuzzle(self, maxSearchDepth=100_000):
        nodes = self.getNodesWithoutValue()
        lastP = 0

        while nodes:

            # get random node
            randomIndex = random.randint(0, len(nodes) - 1)
            x, y = nodes[randomIndex].x, nodes[randomIndex].y

            # get all valid values for this node
            validNumList = [num for num in range(1, 10) if len(self.isNodeValid(nodes[randomIndex], num)) == 0]

            # set the node to a random value for all valid values
            self.setValue(x, y, validNumList[random.randint(0, len(validNumList) - 1)])

            # if the board doesn't have a solution, because of the new value => reset
            # numberOfSolutions = self.backTrackingWithoutRecursion(1, False, maxSearchDepth)
            numberOfSolutions = self.backTrackingWithoutRecursion(1, True, maxSearchDepth)

            # returns -1 if the algorithm searches through 10 000 000 loops without result
            # this puzzle is too costly to generate
            if numberOfSolutions == -1:
                print("\n\n\n ATTENTION: Search has been restarted, current search is too costly \n\n\n")
                return False

            # return 0 if the puzzle has no solution
            if numberOfSolutions == 0:
                self.setValue(x, y, 0)

            else:
                # the node has been successfully generated
                nodes.pop(randomIndex)

            # console
            p = len(nodes)

            p = int(50 - 50 * p / 81)
            if p != lastP:
                print(f"Loading: {p} %")
                lastP = p

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

            # save node value in case the uniqueness of the puzzle breaks down once this node is removed
            value = self.getBoardNode(x, y).value

            # remove node value
            self.setValue(x, y, 0)

            # console output
            p = len(randomNodeList)
            if p == 0:
                p = 1

            p = int(50 + 50 / p)
            if p != lastP:
                print(f"Loading: {p} %")
                lastP = p

            # if the puzzle has two solution => set the node to its original value
            if self.backTrackingWithoutRecursion(2, False, maxSearchDepth) == 2:
                self.setValue(x, y, value)

                # user cannot change this node its apart of the puzzle
                self.getBoardNode(x, y).userCannotChange = True

        return True

    def setToRandomPreGeneratedBoard(self):
        with open('preGeneratedSudokuBoards.csv', 'rt') as f:
            reader = list(csv.reader(f, delimiter=','))
            self.setBoardWithDefaultValues(reader[random.randint(0, sum(1 for _ in reader) - 1)])
        pass

    def setToPreGeneratedBoard(self, index):
        with open('preGeneratedSudokuBoards.csv', 'rt') as f:
            reader = list(csv.reader(f, delimiter=','))
            self.setBoardWithDefaultValues(reader[index])
            
