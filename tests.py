from sudoku import Sudoku
import sudoku_solver as solver
import sudoku_generator as generator 
from time import time



sudoku_grid_00 = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]

sudoku_grid_99 = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 3, 6, 0, 0, 0, 0, 0],
             [0, 7, 0, 0, 9, 0, 2, 0 ,0],
             [0, 5, 0, 0, 0, 7, 0, 0, 0],
             [0, 0, 0, 0, 4, 5, 7, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 3, 0],
             [0, 0, 1, 0, 0, 0, 0, 6, 8],
             [0, 0, 8, 5, 0, 0, 0, 1, 0],
             [0, 9, 0, 0, 0, 0, 4, 0, 0]]

sudoku_grid_01 = [[0, 0, 0, 6, 0, 0, 8, 0, 0], 
             [6, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 1 ,0],
             [0, 0, 0, 0, 6, 0, 2, 0, 0],
             [0, 6, 8, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 5, 3, 0, 0, 0],
             [1, 0, 5, 0, 7, 6, 0, 0, 0],
             [0, 0, 6, 0, 4, 0, 0, 0, 0],
             [0, 0, 4, 0, 0, 0, 0, 0, 0]]

sudoku_02 = Sudoku("6....894.9....61...7..4....2..61..........2...89..2.......6...5.......3.8....16..", ".")

def test_solution(sudoku):
    print(solver.solve(sudoku))


def test_generate():
    generator.print_new_sudoku()



def test_generate_many(number):
    global count
    while count < number:
        count+=1
        generator.print_new_sudoku(hints = 23)

def test_solve_many(file):
    global count
    f = open(file, "r")
    for sudoku in f:
        
        count += 1
        print(solver.solve(Sudoku(sudoku)))
    f.close()



initial_time = time()
count = 0
#test_solution(Sudoku(sudoku_grid_01))

#test_solution(sudoku_02)
#test_generate_many(5)

test_solve_many("generated_sudokus.txt")


if count:
    print(str(count) + " operations.")

print("Time elapsed in seconds:", time() - initial_time)