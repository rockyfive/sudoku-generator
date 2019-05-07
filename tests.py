from sudoku import Sudoku
import sudoku_solver as solver
import sudoku_generator as generator 
from time import time



sudoku_grid_0 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0 ,0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0]]

sudoku_grid_1 = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 3, 6, 0, 0, 0, 0, 0],
                [0, 7, 0, 0, 9, 0, 2, 0 ,0],
                [0, 5, 0, 0, 0, 7, 0, 0, 0],
                [0, 0, 0, 0, 4, 5, 7, 0, 0],
                [0, 0, 0, 1, 0, 0, 0, 3, 0],
                [0, 0, 1, 0, 0, 0, 0, 6, 8],
                [0, 0, 8, 5, 0, 0, 0, 1, 0],
                [0, 9, 0, 0, 0, 0, 4, 0, 0]]

sudoku_grid_2 = [[0, 0, 0, 6, 0, 0, 8, 0, 0], 
                [6, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 1 ,0],
                [0, 0, 0, 0, 6, 0, 2, 0, 0],
                [0, 6, 8, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 5, 3, 0, 0, 0],
                [1, 0, 5, 0, 7, 6, 0, 0, 0],
                [0, 0, 6, 0, 4, 0, 0, 0, 0],
                [0, 0, 4, 0, 0, 0, 0, 0, 0]]

sudoku_string_1 = Sudoku("6....894.9....61...7..4....2..61..........2...89..2.......6...5.......3.8....16..", ".")

def test_solution(sudoku):
    print("Solving a sudoku...")
    initial_time = time()
    print(solver.solve(sudoku))
    print_time(initial_time)



def test_generate():
    print("Generating a sudoku...")
    initial_time = time()
    generator.print_new_sudoku()
    print_time(initial_time)



def test_generate_many(number):
    print("Generating sudokus...")
    initial_time = time()
    count = 0
    while count < number:
        count+=1
        generator.print_new_sudoku(hints = 23)
    print_count(number)
    print_time(initial_time)

def test_solve_many(file):
    print("Solving sudokus...")
    initial_time = time()
    count = 0
    f = open(file, "r")
    for sudoku in f:
        
        count += 1
        solver.solve(Sudoku(sudoku))
    f.close()
    print_count(count)
    print_time(initial_time)

def print_count(n):
    print(str(n) + " operations.")

def print_time(initial_time):
    print("Time elapsed in seconds:", time() - initial_time)


# Launch tests

test_solution(Sudoku(sudoku_grid_1))

test_solution(sudoku_string_1)
test_generate_many(5)

test_solve_many("generated_sudokus.txt")