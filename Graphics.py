import sys
from os.path import exists
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window

pygame.init()
FONT = pygame.font.Font(None, 32)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
RED = (255, 69, 0)
BLUE = (0, 0, 255)


class Graphics:
    def __init__(self, board):

        self.board = board

        # following variables are used to showing how puzzle is being solved
        self.isSolving = False

        self.numberOfSolutions = 0
        self.nodes = None
        self.savedSolution = None
        self.startSearch = {}
        self.index = 0
        self.nodesCopy = None

        # initialize startSearch
        for i in range(self.board.width * self.board.height + 1):
            self.startSearch[i] = 1

        # pixel width of line
        self.BOLD_LINE = 3

        self.SQUARE_SIDE_SIZE = 50

        self.BOARD_HEIGHT = self.BOARD_WIDTH = self.SQUARE_SIDE_SIZE * 9 + self.BOLD_LINE - 1

        # pygame graphics tools
        self.SCREEN = pygame.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.CLOCK.tick(20)
        self.SCREEN.fill(WHITE)

        # selected node cords
        self.selectedX = None
        self.selectedY = None

        # is selected node valid
        self.isValid = True

        # graphical representation of board
        self.numberText = []
        for _ in range(self.board.width):
            line = []
            for _ in range(self.board.height):
                line.append(FONT)
            self.numberText.append(line)

        self.menu = None

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
                    symbol = ""

                color = BLUE

                if self.board.board[y][x].userCannotChange or len(self.board.getNodesWithoutValue()) == 0:
                    color = BLACK

                text = self.numberText[y][x].render(symbol, False, color)
                self.SCREEN.blit(text, (graphicsX, graphicsY))

    def showSelected(self, x, y):

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
        if self.isValid and not self.board.board[y][x].userCannotChange:
            self.SCREEN.fill(GREEN, selectedSquare)
        else:
            self.SCREEN.fill(RED, selectedSquare)

    def evenHandler(self):
        # handle events

        while True:

            self.showBoard()

            if self.isSolving:
                output = self.board.backTrackingWithoutRecursionCycle(self.nodes, self.nodesCopy, self.index,
                                                                      self.startSearch,
                                                                      self.numberOfSolutions)

                if isinstance(output, tuple):
                    # hasn't found solution => update variables
                    self.nodes, self.nodesCopy, self.index, self.startSearch, self.numberOfSolutions, _ = output

                else:
                    # has found solution
                    self.isSolving = False

            isSelected = self.selectedX is not None and self.selectedY is not None

            if isSelected:
                self.showSelected(self.selectedX, self.selectedY)

            self.showNumbersOnBoard()

            mouseX, mouseY = pygame.mouse.get_pos()

            # pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:

                    validInput = "123456789"

                    if event.key == pygame.K_BACKSPACE and not self.board.getBoardNode(self.selectedX,
                                                                                       self.selectedY).userCannotChange:
                        self.board.setValue(self.selectedX, self.selectedY, 0)

                    elif event.key == pygame.K_ESCAPE:
                        self.board.saveBoard()
                        self.createMenu()
                        pygame.quit()
                        break

                    elif event.unicode in validInput and isSelected and not self.isSolving:

                        if not event.unicode == '':

                            if self.board.isNodeValid(self.board.board[self.selectedY][self.selectedX],
                                                      int(event.unicode)) \
                                    and not self.board.getBoardNode(self.selectedX, self.selectedY).userCannotChange:
                                self.board.setValue(self.selectedX, self.selectedY, int(event.unicode))
                                self.isValid = True
                            else:
                                self.isValid = False

                    elif event.key == pygame.K_s:

                        if self.isSolving:
                            self.board.resetNodesOnBoardThatUserChanged()
                            self.isSolving = False

                        else:
                            self.nodes = self.board.getNodesWithoutValue()

                            if len(self.nodes) == 0:
                                self.board.resetNodesOnBoard(self.nodesCopy)

                            else:
                                self.board.resetNodesOnBoardThatUserChanged()
                                self.nodes = self.board.getNodesWithoutValue()
                                self.nodesCopy = self.nodes.copy()
                                self.isSolving = True

                                self.index = 0
                                self.numberOfSolutions = 0
                                self.startSearch = {}
                                for i in range(self.board.width * self.board.height + 1):
                                    self.startSearch[i] = 1

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    indexX = int(mouseX / self.SQUARE_SIDE_SIZE)
                    indexY = int(mouseY / self.SQUARE_SIDE_SIZE)

                    self.selectedX, self.selectedY = indexX, indexY
                    self.isValid = True

            pygame.display.update()

    def loading(self):
        rect = pygame.Rect(10, self.BOARD_WIDTH - 100, self.BOARD_WIDTH - 100, self.SQUARE_SIDE_SIZE)
        self.SCREEN.fill(GREEN, rect)
        pygame.display.update()

    def createMenu(self):
        self.isSolving = False

        def newGame():
            self.board.setToRandomPreGeneratedBoard()
            self.evenHandler()

        def resumeGame():
            self.board.loadBoard()
            self.evenHandler()

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
