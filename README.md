# Sudoku

A desktop Sudoku game built with Python and Pygame, featuring interactive play, note-taking, puzzle loading/saving, and a built-in backtracking solver visualization.

## Project Overview

This project implements a playable 9×9 Sudoku application with a graphical interface. It supports starting a new game from pre-generated boards, resuming a saved game, validating player input against Sudoku rules, and stepping through an automated solve process.

The codebase is organized around a clear separation of concerns:
- `Board` handles game state, validation, persistence, and puzzle generation/loading.
- `Graphics` handles rendering, menu flow, and user input.
- `Solver` handles solving logic (currently backtracking-based in the UI flow).

## Features

- Interactive Sudoku board UI using `pygame`
- Keyboard and mouse input for cell selection and value entry
- Candidate notes mode (right-click to toggle note entry)
- Real-time invalid-entry highlighting
- Save and resume game state via CSV (`savedBoard.csv`)
- Load random puzzles from a pre-generated dataset
- Built-in backtracking solver with visual progression
- Utilities in `Main.py` for dataset validation and solved-board generation

## Architecture / Structure

```text
.
├── Main.py                         # Entry point and dataset utility functions
├── Graphics.py                     # Pygame rendering, menu, input handling
├── Board.py                        # Board model, validation, persistence, generation
├── Solver.py                       # Sudoku solving logic
├── Node.py                         # Cell/node data model
├── preGeneratedSudokuBoards.csv    # Puzzle dataset (givens)
├── preSolvedSudokuBoards.csv       # Solved boards dataset
├── savedBoard.csv                  # Last saved game (created at runtime)
└── SuDoku/
    └── preGeneratedSudokuBoards.csv
```

### Runtime flow

1. `Main.py` initializes a `Board`, then starts `Graphics.createMenu()`.
2. The menu allows creating a new game or resuming a saved one.
3. During gameplay, `Graphics` delegates board logic to `Board` and solving to `Solver`.
4. On exit, current game state can be persisted to `savedBoard.csv`.

## Build & Run Instructions

### Prerequisites

- Python 3.9+
- `pip`

### Install dependencies

```bash
python -m pip install pygame pygame-menu
```

### Run the game

From the project root:

```bash
python Main.py
```

If your system maps Python 3 to `python3`, use:

```bash
python3 Main.py
```

### Controls

- **Arrow keys**: Move selection
- **1–9**: Enter value in selected editable cell
- **Backspace/Delete**: Clear selected editable cell
- **Right-click + number**: Add/remove candidate notes
- **S**: Start/stop solver visualization
- **Space**: Load a new random puzzle
- **Esc**: Save and return to menu

## Testing

This repository currently does not include an automated test suite.

Suggested manual checks:
- Start a new game and verify editable vs fixed cells
- Enter conflicting values and confirm invalid highlighting
- Add/remove notes in a cell
- Run solver (`S`) and verify completion
- Exit and resume to confirm persistence from `savedBoard.csv`

There are helper routines in `Main.py` (`checkDataSet`, `solveAndSaveSuDokuBoard`) that can be used for dataset validation/generation when needed.

## Project Context

This is a Python desktop Sudoku project focused on core gameplay, solver integration, and board-state handling in a lightweight codebase. It is well-suited for learning and experimenting with:
- game-loop and input handling with `pygame`
- Sudoku constraint validation and backtracking
- separating UI, domain model, and solver logic in a small project
