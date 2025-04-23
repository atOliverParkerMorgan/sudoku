import sys
from os.path import exists
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from Solver import Solver

pygame.init()
FONT = pygame.font.Font(None, 32)
NOTE_FONT = pygame.font.Font(None, 25)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
GREY = (128, 128, 128)
RED = (255, 69, 0)
BLUE = (0, 0, 255)
BROWN = (255, 153, 51)
DARK_GREEN = (51, 102, 0)


class Graphics:
    def __init__(self, board):
        self.board = board

        # following variables are used to showing how puzzle is being solved
        self.isSolving = False
        self.numberOfSolutions = 0
        self.emptyNodes = None
        self.savedSolution = None
        self.currentIndex = 0
        self.lastNodeValues = None
        self.invalidNodes = []

        # pixel width of line
        self.BOLD_LINE = 3
        self.SQUARE_SIDE_SIZE = 50
        self.BOARD_HEIGHT = self.BOARD_WIDTH = self.SQUARE_SIDE_SIZE * 9 + self.BOLD_LINE - 1

        # pygame graphics tools
        self.SCREEN = pygame.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.CLOCK.tick(20)
        self.SCREEN.fill(WHITE)

        self.solver = None

        # selected node cords
        self.selectedX = None
        self.selectedY = None

        self.menu = None

        # check for double click
        self.doubleClick = False

        # timer for double click
        self.timer = 0
        self.ADD_TO_TIMER = self.CLOCK.tick(30) / 1000

        self.addingNotes = False

    def isDoubleClick(self):
        self.timer += self.ADD_TO_TIMER
        return self.timer < 3

    def showBoard(self):
        fullScreen = pygame.Rect(0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.SCREEN.fill(WHITE, fullScreen)

        # show lines around on board
        for x in range(0, self.BOARD_WIDTH, self.SQUARE_SIDE_SIZE):
            n = 1
            if x % 3 == 0:
                n = self.BOLD_LINE
            pygame.draw.line(self.SCREEN, BLACK, (x, 0), (x, self.BOARD_HEIGHT), n)

        for y in range(0, self.BOARD_HEIGHT, self.SQUARE_SIDE_SIZE):
            n = 1
            if y % 3 == 0:
                n = self.BOLD_LINE
            pygame.draw.line(self.SCREEN, BLACK, (0, y), (self.BOARD_WIDTH, y), n)

    def showNumbersOnBoard(self):
        # draw symbols on board
        for x, graphicsX in zip(range(self.board.width),
                               range(int(self.SQUARE_SIDE_SIZE / 2) - 5, self.BOARD_WIDTH, self.SQUARE_SIDE_SIZE)):
            for y, graphicsY in zip(range(self.board.height),
                                   range(int(self.SQUARE_SIDE_SIZE / 2) - 8, self.BOARD_HEIGHT,
                                         self.SQUARE_SIDE_SIZE)):

                symbol = str(self.board.board[y][x].value)
                if symbol == "0":
                    note_nums = self.board.getBoardNode(x, y).note_nums
                    biasY = - 15
                    biasX = - 15
                    for note_num in note_nums:
                        if note_num != 0:
                            self.SCREEN.blit(NOTE_FONT.render(str(note_num), False, BROWN), (graphicsX + biasX,
                                                                                            graphicsY + biasY))
                            if biasX == 15:
                                biasX = - 15
                                biasY += 15
                            else:
                                biasX += 15
                else:
                    color = BLUE

                    if self.board.board[y][x].user_cannot_change or len(self.board.getNodesWithoutValue()) == 0:
                        color = BLACK

                    if self.invalidNodes is not None:
                        for node in self.invalidNodes:
                            if x == node[0] and y == node[1]:
                                color = RED

                    text = FONT.render(symbol, False, color)
                    self.SCREEN.blit(text, (graphicsX, graphicsY))

    def showSelected(self, x, y, color):
        # show selected

        # account for lines that separate nodes
        boarderFrontX, boarderFrontY, boarderBackX, boarderBackY = 1, 1, 1, 1
        if x % 3 == 0:
            boarderFrontX = 2
            boarderBackX = 2

        if y % 3 == 0:
            boarderFrontY = 2
            boarderBackY = 2

        if (x + 1) % 3 == 0:
            boarderBackX = 2

        if (y + 1) % 3 == 0:
            boarderBackY = 2

        # create the square using rect
        selectedSquare = pygame.Rect(x * self.SQUARE_SIDE_SIZE + boarderFrontX,
                                    y * self.SQUARE_SIDE_SIZE + boarderFrontY,
                                    self.SQUARE_SIDE_SIZE - boarderBackX,
                                    self.SQUARE_SIDE_SIZE - boarderBackY)

        # change color depending if current user input is valid or not
        self.SCREEN.fill(color, selectedSquare)

    def eventHandler(self):
        # handle events
        while True:
            self.showBoard()

            if self.isSolving:
                self.currentIndex, solutionsFound = self.solver.backtracking_solver_tick(
                    self.lastNodeValues, 
                    self.currentIndex,
                    self.emptyNodes, 
                    self.numberOfSolutions
                )
                
                if self.currentIndex == -1:
                    # Solution found or no more solutions possible
                    self.isSolving = False

            isSelected = self.selectedX is not None and self.selectedY is not None

            if isSelected:
                for x in range(self.board.width):
                    self.showSelected(x, self.selectedY, GREY)

                for y in range(self.board.width):
                    self.showSelected(self.selectedX, y, GREY)

                startRow = self.selectedX - self.selectedX % 3
                startCol = self.selectedY - self.selectedY % 3

                for x in range(3):
                    for y in range(3):
                        self.showSelected(startRow + x, startCol + y, GREY)

                if self.addingNotes:
                    self.showSelected(self.selectedX, self.selectedY, DARK_GREEN)
                elif not self.board.board[self.selectedY][self.selectedX].user_cannot_change:
                    self.showSelected(self.selectedX, self.selectedY, GREEN)
                else:
                    self.showSelected(self.selectedX, self.selectedY, BLUE)

            self.showNumbersOnBoard()

            mouseX, mouseY = pygame.mouse.get_pos()

            # pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.board.saveBoard()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    validInput = "123456789"

                    if event.key == pygame.K_BACKSPACE and not self.board.getBoardNode(self.selectedX,
                                                                                      self.selectedY).user_cannot_change:
                        self.board.setValue(self.selectedX, self.selectedY, 0)

                    elif event.key == pygame.K_ESCAPE:
                        self.board.saveBoard()
                        self.createMenu()
                        pygame.quit()
                        break

                    elif event.unicode in validInput and isSelected and not self.isSolving:
                        if not event.unicode == '':
                            node = self.board.getBoardNode(self.selectedX, self.selectedY)
                            inputValue = str(event.unicode)

                            if self.addingNotes:
                                if inputValue in node.noteNums:
                                    node.noteNums.remove(inputValue)
                                else:
                                    node.noteNums.append(inputValue)
                                    node.noteNums.sort()

                            elif not self.board.getBoardNode(self.selectedX, self.selectedY).user_cannot_change:
                                if self.board.getBoardNode(self.selectedX, self.selectedY).value == int(event.unicode):
                                    self.board.setValue(self.selectedX, self.selectedY, 0)
                                else:
                                    self.board.setValue(self.selectedX, self.selectedY, int(event.unicode))
                                    self.invalidNodes = self.board.isNodeValid(
                                        self.selectedX, self.selectedY,
                                        int(event.unicode))

                                    # the input is valid
                                    if len(self.invalidNodes) == 1:
                                        self.invalidNodes = []

                    elif event.key == pygame.K_s:
                        self.solver = Solver(self.board, "backtracking", 1)

                        if self.isSolving:
                            self.board.resetNodesOnBoardThatUserChanged()
                            self.isSolving = False
                        else:
                            self.emptyNodes = self.board.getNodesWithoutValue()

                            if len(self.emptyNodes) == 0:
                                self.board.resetNodesOnBoard(self.emptyNodes)
                            else:
                                self.board.resetNodesOnBoardThatUserChanged()
                                self.emptyNodes = self.board.getNodesWithoutValue()
                                self.isSolving = True

                                self.currentIndex = 0
                                self.numberOfSolutions = 0
                                self.lastNodeValues = {}
                                
                                # Initialize lastNodeValues for each empty node
                                for node in self.emptyNodes:
                                    self.lastNodeValues[node] = 1

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.addingNotes = event.button == 3

                    indexX = int(mouseX / self.SQUARE_SIDE_SIZE)
                    indexY = int(mouseY / self.SQUARE_SIDE_SIZE)

                    self.selectedX, self.selectedY = indexX, indexY
                    self.invalidNodes = []

                    if self.isDoubleClick() and self.doubleClick:
                        self.selectedX, self.selectedY = None, None
                        self.doubleClick = False
                        self.addingNotes = False
                    else:
                        self.timer = 0
                        self.doubleClick = True

            if self.doubleClick:
                self.isDoubleClick()

            pygame.display.update()

    def loading(self):
        rect = pygame.Rect(10, self.BOARD_WIDTH - 100, self.BOARD_WIDTH - 100, self.SQUARE_SIDE_SIZE)
        self.SCREEN.fill(GREEN, rect)
        pygame.display.update()

    def createMenu(self):
        self.isSolving = False

        def newGame():
            self.board.setToRandomPreGeneratedBoard()
            self.eventHandler()

        def resumeGame():
            self.board.loadBoard()
            self.eventHandler()

        # create menu
        surface = create_example_window('SuDoku - Hint: PRESS "S" TO SOLVE',
                                      (self.BOARD_WIDTH, self.BOARD_HEIGHT))

        self.menu = pygame_menu.Menu('SuDoku', self.BOARD_WIDTH, self.BOARD_HEIGHT,
                                   theme=pygame_menu.themes.THEME_DARK)

        self.menu.add.button('NEW GAME', newGame)
        if exists("savedBoard.csv"):
            self.menu.add.button('RESUME', resumeGame)

        self.menu.add.button('QUIT', pygame_menu.events.EXIT)
        self.menu.add.label('')

        self.menu.add.label("Oliver Morgan")

        self.menu.mainloop(surface)