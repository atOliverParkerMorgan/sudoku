from Board import Board
from Solver import Solver
import time
import matplotlib.pyplot as plt

def compareSolvers(iterations=100, difficulties=[0.25, 0.5, 0.75, 0.95]):
    sizes = [9, 16]
    solver_types = ["minimum-remaining-values", "least-constraining-values"]
    results = {solver_type: [] for solver_type in solver_types}

    for difficulty in difficulties:
        for solver_type in solver_types:
            start_time = time.time()
            for _ in range(iterations):
                for size in sizes:
                    b = Board(size)
                    b.generatePuzzle(difficulty)
                    s = Solver(b, solver_type)
                    s.solve()
            end_time = time.time()
            elapsed = end_time - start_time
            print(f"{solver_type} | Difficulty: {difficulty} | Time: {elapsed:.2f}s")
            results[solver_type].append(elapsed)
    
    return results, difficulties

if __name__ == '__main__':
    iterations = 100
    difficulties = [0.25, 0.5, 0.75, 0.95]
    results, difficulties = compareSolvers(iterations, difficulties)

    for solver_type, times in results.items():
        plt.plot(difficulties, times, label=solver_type, marker='o')

    plt.title(f'Solver Performance vs Difficulty ({iterations} iterations per point)')
    plt.xlabel('Puzzle Difficulty')
    plt.ylabel('Elapsed Time (s)')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
