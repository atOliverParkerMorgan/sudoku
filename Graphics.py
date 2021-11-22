import pygame


class Graphics:
    def __init__(self):
        self.SQUARE_SIDE_SIZE = 50
        self.BOLD_LINE = 3
        self.BOARD_HEIGHT = self.BOARD_WIDTH = self.SQUARE_SIDE_SIZE * 9 + self.BOLD_LINE - 1
        pygame.init()

        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        # pygame graphics tools
        self.SCREEN = pygame.display.set_mode((self.BOARD_WIDTH, self.BOARD_HEIGHT))
        self.CLOCK = pygame.time.Clock()
        self.CLOCK.tick(20)
        self.SCREEN.fill(self.WHITE)

    def showBoard(self):
        for x in range(0, self.BOARD_WIDTH, self.SQUARE_SIDE_SIZE):
            n = 1
            if x % 3 == 0:
                n = self.BOLD_LINE
            pygame.draw.line(self.SCREEN, self.BLACK, (x, 0), (x, self.BOARD_HEIGHT), n)
        for y in range(0, self.BOARD_HEIGHT, self.SQUARE_SIDE_SIZE):
            n = 1
            if y % 3 == 0:
                n = self.BOLD_LINE
            pygame.draw.line(self.SCREEN, self.BLACK, (0, y), (self.BOARD_WIDTH, y), n)

    def evenHandler(self, ):
        while True:
            # graphics
            self.showBoard()

            # pygame events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    pass

                if event.type == pygame.MOUSEBUTTONDOWN:
                    pass

                elif event.type == pygame.MOUSEBUTTONUP:
                    pass

            pygame.display.update()
