import pygame

pygame.init()
FONT = pygame.font.Font(None, 32)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (34, 139, 34)


class Graphics:
    def __init__(self, board):

        self.board = board
        self.SQUARE_SIDE_SIZE = 50
        self.BOLD_LINE = 3
        self.BOARD_HEIGHT = self.BOARD_WIDTH = self.SQUARE_SIDE_SIZE * 9 + self.BOLD_LINE - 1

        # pygame graphics tools
        self.SCREEN = pygame.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.CLOCK.tick(20)
        self.SCREEN.fill(WHITE)

        self.selectedX = None
        self.selectedY = None

        self.numberText = []
        for _ in range(self.board.width):
            line = []
            for _ in range(self.board.height):
                line.append(FONT)
            self.numberText.append(line)

    def showBoard(self):

        fullScreen = pygame.Rect(0, 0, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.SCREEN.fill(WHITE, fullScreen)

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
        for x, graphicsX in zip(range(self.board.width),
                                range(int(self.SQUARE_SIDE_SIZE / 2) - 5, self.BOARD_WIDTH, self.SQUARE_SIDE_SIZE)):
            for y, graphicsY in zip(range(self.board.height),
                                    range(int(self.SQUARE_SIDE_SIZE / 2) - 8, self.BOARD_HEIGHT,
                                          self.SQUARE_SIDE_SIZE)):
                text = self.numberText[y][x].render(str(self.board.board[y][x].value), False, BLACK)
                self.SCREEN.blit(text, (graphicsX, graphicsY))

    def showSelected(self, x, y):
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

        selectedSquare = pygame.Rect(x * self.SQUARE_SIDE_SIZE + boarderFrontX,
                                     y * self.SQUARE_SIDE_SIZE + boarderFrontY,
                                     self.SQUARE_SIDE_SIZE - boarderBackX,
                                     self.SQUARE_SIDE_SIZE - boarderBackY)
        self.SCREEN.fill(GREEN, selectedSquare)

    def evenHandler(self):
        while True:

            self.showBoard()

            isSelected = self.selectedX is not None and self.selectedY is not None

            if isSelected:
                self.showSelected(self.selectedX, self.selectedY)

            self.showNumbersOnBoard()

            mouseX, mouseY = pygame.mouse.get_pos()

            # pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    print("keydown")
                    print(isSelected)
                    print(event.key)
                    if event.key == pygame.K_1 and isSelected:
                        print("K_1")
                        originalValue = self.board.getBoardNode(self.selectedX, self.selectedY).value
                        self.board.setValue(self.selectedX, self.selectedY, 1)
                        if not self.board.isNodeValid(self.board.board[self.selectedY][self.selectedX]):
                            self.board.setValue(self.selectedX, self.selectedY, originalValue)


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    indexX = int(mouseX / self.SQUARE_SIDE_SIZE)
                    indexY = int(mouseY / self.SQUARE_SIDE_SIZE)

                    self.selectedX, self.selectedY = indexX, indexY




                elif event.type == pygame.MOUSEBUTTONUP:
                    pass

            pygame.display.update()
