import sys
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from Solver import Solver
from Board import Board
import random
from os.path import exists

pygame.init()

# Fonts and colors
FONT = pygame.font.Font(None, 32)
NOTE_FONT = pygame.font.Font(None, 25)
BLACK, WHITE, GREEN, GREY, RED, BLUE, BROWN, DARK_GREEN = (
    (0, 0, 0), (255, 255, 255), (34, 139, 34), (128, 128, 128),
    (255, 69, 0), (0, 0, 255), (255, 153, 51), (51, 102, 0)
)


class Graphics:
    def __init__(self, board):
        self.board = board
        self.isSolving = False
        self.solver = None
        self.emptyNodes, self.invalidNodes = [], []

        self.SQUARE_SIDE_SIZE = 50
        self.BOLD_LINE = 3
        self.BOARD_SIZE_PIXELS = self.SQUARE_SIDE_SIZE * board.size + self.BOLD_LINE - 1
        self.SCREEN = pygame.display.set_mode((self.BOARD_SIZE_PIXELS,) * 2)
        self.CLOCK = pygame.time.Clock()
        self.SCREEN.fill(WHITE)

        self.selectedX = self.selectedY = None
        self.addingNotes = False

        self.inputBuffer = ""
        self.lastInputTime = 0
        self.doubleClick = False
        self.timer = 0
        self.ADD_TO_TIMER = self.CLOCK.tick(30) / 1000

    def isDoubleClick(self):
        self.timer += self.ADD_TO_TIMER
        return self.timer < 3

    def showBoard(self):
        self.SCREEN.fill(WHITE)
        box_size = int(self.board.size ** 0.5)

        for i in range(0, self.BOARD_SIZE_PIXELS + 1, self.SQUARE_SIDE_SIZE):
            lw = self.BOLD_LINE if i % (self.SQUARE_SIDE_SIZE * box_size) == 0 else 1
            pygame.draw.line(self.SCREEN, BLACK, (i, 0), (i, self.BOARD_SIZE_PIXELS), lw)
            pygame.draw.line(self.SCREEN, BLACK, (0, i), (self.BOARD_SIZE_PIXELS, i), lw)

    def showNumbersOnBoard(self):
        for x in range(self.board.size):
            graphicsX = x * self.SQUARE_SIDE_SIZE + self.SQUARE_SIDE_SIZE // 2 - 5
            for y in range(self.board.size):
                graphicsY = y * self.SQUARE_SIDE_SIZE + self.SQUARE_SIDE_SIZE // 2 - 8
                node = self.board.board[y][x]

                if node.value == 0:
                    biasX = biasY = -15
                    for n in node.note_nums:
                        if n:
                            self.SCREEN.blit(NOTE_FONT.render(str(n), False, BROWN),
                                             (graphicsX + biasX, graphicsY + biasY))
                            biasX, biasY = (biasX + 15, biasY) if biasX < 15 else (-15, biasY + 15)
                else:
                    color = (
                        RED if (x, y) in self.invalidNodes else
                        GREEN if not node.user_cannot_change and not self.board.getNodesWithoutValue()
                        else BLACK if node.user_cannot_change else BLUE
                    )
                    self.SCREEN.blit(FONT.render(str(node.value), False, color), (graphicsX, graphicsY))

    def showSelected(self, x, y, color):
        box_size = int(self.board.size ** 0.5)
        frontX = 2 if x % box_size == 0 else 1
        frontY = 2 if y % box_size == 0 else 1
        backX = 2 if (x + 1) % box_size == 0 else 1
        backY = 2 if (y + 1) % box_size == 0 else 1

        rect = pygame.Rect(x * self.SQUARE_SIDE_SIZE + frontX,
                           y * self.SQUARE_SIDE_SIZE + frontY,
                           self.SQUARE_SIDE_SIZE - backX,
                           self.SQUARE_SIDE_SIZE - backY)
        self.SCREEN.fill(color, rect)

    def initializeSolving(self):
        self.emptyNodes = self.board.getNodesWithoutValue()
        self.invalidNodes = []
        return bool(self.emptyNodes)

    def eventHandler(self):
        while True:
            self.showBoard()

            if self.isSolving and self.solver and self.emptyNodes:
                try:
                    if self.solver.solver_tick():
                        self.isSolving = False
                        if not self.board.getNodesWithoutValue():
                            print("Solution found!")
                        else:
                            print("No solution exists.")
                except Exception as e:
                    print(f"Solver error: {e}")
                    self.isSolving = False

            if self.selectedX is not None and self.selectedY is not None:
                box_size = int(self.board.size ** 0.5)
                sr, sc = self.selectedX - self.selectedX % box_size, self.selectedY - self.selectedY % box_size
                for i in range(self.board.size):
                    self.showSelected(i, self.selectedY, GREY)
                    self.showSelected(self.selectedX, i, GREY)
                for dx in range(box_size):
                    for dy in range(box_size):
                        self.showSelected(sr + dx, sc + dy, GREY)

                cell = self.board.board[self.selectedY][self.selectedX]
                if self.addingNotes:
                    self.showSelected(self.selectedX, self.selectedY, DARK_GREEN)
                elif not cell.user_cannot_change:
                    self.showSelected(self.selectedX, self.selectedY, GREEN)
                else:
                    self.showSelected(self.selectedX, self.selectedY, BLUE)

            self.showNumbersOnBoard()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.board.saveBoard()
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.board.saveBoard()
                        self.createMenu()
                        pygame.quit()
                        return

                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP):
                        self.selectedX = 0 if self.selectedX is None else (self.selectedX + (event.key == pygame.K_RIGHT) - (event.key == pygame.K_LEFT)) % self.board.size
                        self.selectedY = 0 if self.selectedY is None else (self.selectedY + (event.key == pygame.K_DOWN) - (event.key == pygame.K_UP)) % self.board.size

                    elif event.key in (pygame.K_BACKSPACE, pygame.K_DELETE) and self.selectedX is not None:
                        node = self.board.getBoardNode(self.selectedX, self.selectedY)
                        if not node.user_cannot_change:
                            self.board.setValue(self.selectedX, self.selectedY, 0)
                            if event.key == pygame.K_DELETE:
                                node.note_nums.clear()
                                self.selectedX = self.selectedY = None
                                self.doubleClick = False
                            self.invalidNodes.clear()

                    elif event.key == pygame.K_SPACE:
                        if self.isSolving:
                            self.board.resetNodesOnBoardThatUserChanged()
                            self.isSolving = False
                        else:
                            self.board.setToRandomPreGeneratedBoard()
                            return self.eventHandler()

                    elif event.key == pygame.K_s and not self.isSolving:
                        self.solver = Solver(self.board, "minimum-remaining-values")
                        self.isSolving = self.initializeSolving()

                    elif event.unicode.isdigit() and self.selectedX is not None and not self.isSolving:
                        now = pygame.time.get_ticks()
                        if now - self.lastInputTime > 500:
                            self.inputBuffer = ""
                        self.inputBuffer += event.unicode
                        self.lastInputTime = now
                        try:
                            val = int(self.inputBuffer)
                            if 1 <= val <= self.board.size:
                                node = self.board.getBoardNode(self.selectedX, self.selectedY)
                                if self.addingNotes:
                                    node.note_nums = sorted(set(node.note_nums) ^ {val})
                                elif not node.user_cannot_change:
                                    self.invalidNodes.clear()
                                    self.board.setValue(self.selectedX, self.selectedY, 0 if node.value == val else val)
                                    if node.value != val:
                                        self.invalidNodes = self.board.getInvalidityReasons(self.selectedX, self.selectedY, val)
                            if val > self.board.size:
                                self.inputBuffer = ""
                        except ValueError:
                            self.inputBuffer = ""

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()
                    self.addingNotes = (event.button == 3)
                    ix, iy = mx // self.SQUARE_SIDE_SIZE, my // self.SQUARE_SIDE_SIZE
                    if 0 <= ix < self.board.size and 0 <= iy < self.board.size:
                        if self.isDoubleClick() and self.doubleClick:
                            self.selectedX = self.selectedY = None
                            self.addingNotes = self.doubleClick = False
                        else:
                            self.timer = 0
                            self.doubleClick = True
                            self.selectedX, self.selectedY = ix, iy

            if self.doubleClick:
                self.isDoubleClick()

            pygame.display.update()

    def createMenu(self):
        self.isSolving = False
        board_size = [16]
        difficulty = 0.5

        def set_board_size(_, val): board_size[0] = val

        def set_difficulty(_, val): difficulty = val

        def start_game(solver_type=None):
            self.__init__(Board(board_size[0]))
            if solver_type:
                self.board.generatePuzzle(difficulty)
                self.solver = Solver(self.board, solver_type)
                self.isSolving = self.initializeSolving()
            self.eventHandler()

        def resume_game():
            self.__init__(Board(board_size[0]))
            self.board.loadBoard(f'saved_{self.board.size}x{self.board.size}', 0)
            self.eventHandler()

        surface = create_example_window('SuDoku - Hint: PRESS "S" TO SOLVE', (self.BOARD_SIZE_PIXELS,) * 2)
        self.menu = pygame_menu.Menu('SuDoku', self.BOARD_SIZE_PIXELS, self.BOARD_SIZE_PIXELS,
                                     theme=pygame_menu.themes.THEME_DARK)
        self.menu.add.selector('Board Size ', [('16x16', 16), ('9x9', 9), ('4x4', 4)], onchange=set_board_size)
        self.menu.add.selector('Difficutly ', [ ('Medium', 0.5), ('Easy', 0.25), ('Hard', 0.75), ('Impossible', 0.95)], onchange=set_board_size)

        self.menu.add.button('NEW GAME', lambda: start_game())

        if exists("savedBoard.csv"):
            self.menu.add.button('RESUME', resume_game)

        self.menu.add.button('Minimum Remaining Values', lambda: start_game("minimum-remaining-values"))
        self.menu.add.button('Least Constraining Values', lambda: start_game("least-constraining-values"))
        self.menu.add.button('QUIT', pygame_menu.events.EXIT)
        self.menu.add.label('')
        self.menu.add.label("Oliver Morgan")

        self.menu.mainloop(surface)
