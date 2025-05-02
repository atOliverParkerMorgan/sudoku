import sys
from os.path import exists
import pygame
import pygame_menu
from pygame_menu.examples import create_example_window
from Solver import Solver
import random
from Board import Board

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
        self.emptyNodes = []  # Initialize as empty list instead of None
        self.savedSolution = None
        self.currentIndex = 0
        self.lastNodeValues = {}  # Initialize as empty dict instead of None
        self.invalidNodes = []
        self.foundSolution = False

        # pixel width of line
        self.BOLD_LINE = 3
        self.SQUARE_SIDE_SIZE = 50
        self.BOARD_SIZE_PIXELS = self.SQUARE_SIDE_SIZE * board.size + self.BOLD_LINE - 1

        # pygame graphics tools
        self.SCREEN = pygame.display.set_mode((self.BOARD_SIZE_PIXELS, self.BOARD_SIZE_PIXELS))
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

        self.inputBuffer = ""
        self.lastInputTime = 0

    def isDoubleClick(self):
        self.timer += self.ADD_TO_TIMER
        return self.timer < 3

    def showBoard(self):
        fullScreen = pygame.Rect(0, 0, self.BOARD_SIZE_PIXELS, self.BOARD_SIZE_PIXELS)
        self.SCREEN.fill(WHITE, fullScreen)

        # Calculate the box size (e.g., 3 for 9x9 grid)
        box_size = int(self.board.size ** 0.5)

        # show lines around on board
        for x in range(0, self.BOARD_SIZE_PIXELS + 1, self.SQUARE_SIDE_SIZE):
            n = 1
            if x % (self.SQUARE_SIDE_SIZE * box_size) == 0:
                n = self.BOLD_LINE
            pygame.draw.line(self.SCREEN, BLACK, (x, 0), (x, self.BOARD_SIZE_PIXELS), n)

        for y in range(0, self.BOARD_SIZE_PIXELS + 1, self.SQUARE_SIDE_SIZE):
            n = 1
            if y % (self.SQUARE_SIDE_SIZE * box_size) == 0:
                n = self.BOLD_LINE
            pygame.draw.line(self.SCREEN, BLACK, (0, y), (self.BOARD_SIZE_PIXELS, y), n)

    def showNumbersOnBoard(self):
        # draw symbols on board
        for x, graphicsX in zip(range(self.board.size),
                               range(int(self.SQUARE_SIDE_SIZE / 2) - 5, self.BOARD_SIZE_PIXELS, self.SQUARE_SIDE_SIZE)):
            for y, graphicsY in zip(range(self.board.size),
                                   range(int(self.SQUARE_SIDE_SIZE / 2) - 8, self.BOARD_SIZE_PIXELS,
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

                    if self.board.board[y][x].user_cannot_change:
                        color = BLACK
                    
                    if len(self.board.getNodesWithoutValue()) == 0:
                        color = GREEN

                    if self.invalidNodes:
                        for node in self.invalidNodes:
                            if node[0] == x and node[1] == y:
                                color = RED
                                break

                    text = FONT.render(symbol, False, color)
                    self.SCREEN.blit(text, (graphicsX, graphicsY))

    def showSelected(self, x, y, color):
        # Calculate box size (e.g., 3 for 9x9 grid)
        box_size = int(self.board.size ** 0.5)
        
        # show selected
        # account for lines that separate nodes
        boarderFrontX, boarderFrontY, boarderBackX, boarderBackY = 1, 1, 1, 1
        if x % box_size == 0:
            boarderFrontX = 2
            boarderBackX = 2

        if y % box_size == 0:
            boarderFrontY = 2
            boarderBackY = 2

        if (x + 1) % box_size == 0:
            boarderBackX = 2

        if (y + 1) % box_size == 0:
            boarderBackY = 2

        # create the square using rect
        selectedSquare = pygame.Rect(x * self.SQUARE_SIDE_SIZE + boarderFrontX,
                                    y * self.SQUARE_SIDE_SIZE + boarderFrontY,
                                    self.SQUARE_SIDE_SIZE - boarderBackX,
                                    self.SQUARE_SIDE_SIZE - boarderBackY)

        # change color depending if current user input is valid or not
        self.SCREEN.fill(color, selectedSquare)

    def initializeSolving(self):
        """Initialize variables for the solving process"""
        self.emptyNodes = self.board.getNodesWithoutValue()
        
        # Handle case where there are no empty nodes
        if not self.emptyNodes:
            return False
        
        # Reset solver state
        if self.solver:
            self.solver.number_of_solutions = 0
            self.solver.backtracking_nodes = []
            
            # Apply forward checking to prepare the board
            self.solver.apply_forward_checking()
        
        self.currentIndex = 0
        self.numberOfSolutions = 0
        self.lastNodeValues = {}
        
        # Initialize lastNodeValues for each empty node
        for node in self.emptyNodes:
            self.lastNodeValues[node] = 0
            
        return True

    def eventHandler(self):
        # handle events
        while True:
            self.showBoard()

            if self.isSolving and self.solver:
            # Make sure we have valid empty nodes and initialization
                if not self.emptyNodes:
                    if not self.initializeSolving():
                        self.isSolving = False
                
                # Only proceed if we have valid setup
                if self.isSolving and self.emptyNodes:
                    try:
                    # Get solving result
                        result = self.solver.backtracking_solver_tick(1)  # Pass target_solutions=1
                        
                        # If solver returned True, we're done (either found solution or exhausted possibilities)
                        if result:
                            self.isSolving = False
                            if len(self.board.getNodesWithoutValue()) == 0:
                                print("Solution found!")
                            else:
                                print("No solution exists for this board")
                                
                    except Exception as e:
                        print(f"Error during solving: {e}")
                        self.isSolving = False

            isSelected = self.selectedX is not None and self.selectedY is not None

            if isSelected:
                # Highlight row
                for x in range(self.board.size):
                    self.showSelected(x, self.selectedY, GREY)

                # Highlight column
                for y in range(self.board.size):
                    self.showSelected(self.selectedX, y, GREY)

                # Calculate box size
                box_size = int(self.board.size ** 0.5)
                
                # Highlight the box containing the selected cell
                startRow = self.selectedX - self.selectedX % box_size
                startCol = self.selectedY - self.selectedY % box_size

                for x in range(box_size):
                    for y in range(box_size):
                        self.showSelected(startRow + x, startCol + y, GREY)

                # Highlight the selected cell with appropriate color
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

                    # Handle keyboard navigation
                    if event.key == pygame.K_RIGHT:
                        if self.selectedX is None or self.selectedY is None:
                            self.selectedX, self.selectedY = 0, 0
                        else:
                            self.selectedX = (self.selectedX + 1) % self.board.size
                    
                    elif event.key == pygame.K_LEFT:
                        if self.selectedX is None or self.selectedY is None:
                            self.selectedX, self.selectedY = self.board.size-1, 0
                        else:
                            self.selectedX = (self.selectedX - 1) % self.board.size
                    
                    elif event.key == pygame.K_DOWN:
                        if self.selectedX is None or self.selectedY is None:
                            self.selectedX, self.selectedY = 0, 0
                        else:
                            self.selectedY = (self.selectedY + 1) % self.board.size
                    
                    elif event.key == pygame.K_UP:
                        if self.selectedX is None or self.selectedY is None:
                            self.selectedX, self.selectedY = 0, self.board.size-1
                        else:
                            self.selectedY = (self.selectedY - 1) % self.board.size

                    elif isSelected and event.key == pygame.K_BACKSPACE and not self.board.getBoardNode(self.selectedX,
                                                                                    self.selectedY).user_cannot_change:
                        self.board.setValue(self.selectedX, self.selectedY, 0)
                        self.invalidNodes = []

                    elif event.key == pygame.K_ESCAPE:
                        self.board.saveBoard()
                        self.createMenu()
                        pygame.quit()
                        break

                    elif event.unicode.isdigit() and isSelected and not self.isSolving:
                        now = pygame.time.get_ticks()

                        # Reset buffer if more than 1 second passed
                        if now - self.lastInputTime > 500:
                            self.inputBuffer = ""
                        
                        self.inputBuffer += event.unicode

                        self.lastInputTime = now

                        try:
                            inputValue = int(self.inputBuffer)
                            if 1 <= inputValue <= self.board.size:
                                node = self.board.getBoardNode(self.selectedX, self.selectedY)

                                if self.addingNotes:
                                    if inputValue in node.note_nums:
                                        node.note_nums.remove(inputValue)
                                    else:
                                        node.note_nums.append(inputValue)
                                        node.note_nums.sort()
                                elif not node.user_cannot_change:
                                    self.invalidNodes = []  # Clear any previous invalid nodes
                                    if node.value == inputValue:
                                        self.board.setValue(self.selectedX, self.selectedY, 0)
                                    else:
                                        if not self.board.setValue(self.selectedX, self.selectedY, inputValue):
                                            self.invalidNodes = self.board.getInvalidityReasons(self.selectedX, self.selectedY, inputValue)

                                # Clear buffer after valid input
                                self.inputBuffer = ""
                                
                            elif inputValue > self.board.size:
                                # Clear buffer if input exceeds board max value
                                self.inputBuffer = ""
                        except ValueError:
                            self.inputBuffer = ""


                    elif event.key == pygame.K_DELETE:
                        if isSelected and not self.board.getBoardNode(self.selectedX, self.selectedY).user_cannot_change:
                            self.board.setValue(self.selectedX, self.selectedY, 0)
                            self.board.getBoardNode(self.selectedX, self.selectedY).note_nums = []
                            self.addingNotes = False
                            self.selectedX, self.selectedY = None, None
                            self.doubleClick = False
                            self.invalidNodes = []
                    
                    elif event.key == pygame.K_SPACE:
                        if self.isSolving:
                            self.board.resetNodesOnBoardThatUserChanged()
                            self.isSolving = False
                            self.invalidNodes = []
                        else:
                            self.board.setToRandomPreGeneratedBoard()
                            self.eventHandler()
                    elif event.key == pygame.K_s:
                        # Start solving the current board
                        if not self.isSolving:
                            self.solver = Solver(self.board, "minimum-remaining-values")
                            
                            # Initialize properly before starting
                            if self.initializeSolving():
                                self.isSolving = True


                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.addingNotes = event.button == 3

                    indexX = int(mouseX / self.SQUARE_SIDE_SIZE)
                    indexY = int(mouseY / self.SQUARE_SIDE_SIZE)

                    # Make sure we don't select outside the board
                    if 0 <= indexX < self.board.size and 0 <= indexY < self.board.size:
                        self.selectedX, self.selectedY = indexX, indexY

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
        rect = pygame.Rect(10, self.BOARD_SIZE_PIXELS - 100, self.BOARD_SIZE_PIXELS - 100, self.SQUARE_SIDE_SIZE)
        self.SCREEN.fill(GREEN, rect)
        pygame.display.update()

    def createMenu(self):
        self.isSolving = False
        board_size = [16]  # default value as a list to allow inner modification

        def set_board_size(selected, value):
            board_size[0] = value

        def newGame():
            self.board = Board(board_size[0])
            self.__init__(self.board)  # reinitialize everything with new board
            self.board.loadBoard(f'puzzles_{self.board.size}x{self.board.size}', random.randint(0, 64))
            self.eventHandler()

        def resumeGame():
            self.board = Board(board_size[0])
            self.__init__(self.board)
            self.board.loadBoard(f'saved_{self.board.size}x{self.board.size}', 0)
            self.eventHandler()

        def minimum_remaining_values():
            self.board = Board(board_size[0])
            self.__init__(self.board)
            self.board.loadBoard(f'puzzles_{self.board.size}x{self.board.size}', random.randint(0, 64))
            self.solver = Solver(self.board, "minimum-remaining-values")
            
            # Initialize properly before starting
            if self.initializeSolving():
                self.isSolving = True
            
            self.eventHandler()

        def least_constraining_values():
            self.board = Board(board_size[0])
            self.__init__(self.board)
            self.board.loadBoard(f'puzzles_{self.board.size}x{self.board.size}', random.randint(0, 64))
            self.solver = Solver(self.board, "least-constraining-values")
            
            # Initialize properly before starting
            if self.initializeSolving():
                self.isSolving = True
                
            self.eventHandler()

        surface = create_example_window('SuDoku - Hint: PRESS "S" TO SOLVE',
                                        (self.BOARD_SIZE_PIXELS, self.BOARD_SIZE_PIXELS))

        self.menu = pygame_menu.Menu('SuDoku', self.BOARD_SIZE_PIXELS, self.BOARD_SIZE_PIXELS,
                                    theme=pygame_menu.themes.THEME_DARK)

        self.menu.add.selector('Board Size ',
                            [ ('16x16', 16), ('9x9', 9),('4x4', 4)],
                            onchange=set_board_size)

        self.menu.add.button('NEW GAME', newGame)
        if exists("savedBoard.csv"):
            self.menu.add.button('RESUME', resumeGame)

        self.menu.add.button('Minimum Remaining Values', minimum_remaining_values)
        self.menu.add.button('Least Constraining Values', least_constraining_values)

        self.menu.add.button('QUIT', pygame_menu.events.EXIT)
        self.menu.add.label('')
        self.menu.add.label("Oliver Morgan")

        self.menu.mainloop(surface)

    def setToRandomPreGeneratedBoard(self):
        if hasattr(self.board, 'setToRandomPreGeneratedBoard'):
            self.board.setToRandomPreGeneratedBoard()
        else:
            try:
                self.board.loadBoard(f'puzzles_{self.board.size}x{self.board.size}', random.randint(0, 64))
            except Exception as e:
                print(f"Error loading random board: {e}")