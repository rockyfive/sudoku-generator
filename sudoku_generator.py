# Sudoku generator 2015

from sudoku_solver import solve
from sudoku import Sudoku
import random
import time

HINT_NUMBER = 28

EXTRA_HINTS = 2

def initialize_random_sudoku():
    sudoku = Sudoku()
    box_list = list(sudoku.sudoku_list)
    random.shuffle(box_list)

    hints = list(range(1, 10))
    hints.pop(random.randrange(9))
    box = 0
    for number in range(HINT_NUMBER - 8):
        hints.append(random.randrange(1, 10))
    
    random.shuffle(hints)
    
    while hints and (box < len(box_list)):
        if (len(box_list[box].possible_values) > 1) and hints[0] in box_list[box].possible_values:
            sudoku.play_idx(hints.pop(0), box_list[box].idx)

        box += 1
        
    return sudoku

def generate(hints = HINT_NUMBER, extra_hints = EXTRA_HINTS):    
    new_sudoku = initialize_random_sudoku()
    hints = extra_hints
    check_sudoku = solve(new_sudoku.clone(), True)
    while check_sudoku and (check_sudoku != "Timeout"):
        if type(check_sudoku) == tuple:
            if not hints:
                return generate(extra_hints)
                
            new_sudoku.play_idx(check_sudoku[0], check_sudoku[1])
            check_sudoku = solve(new_sudoku.clone(), True)
            hints -= 1
            continue
        return new_sudoku
        
    return generate(extra_hints)


def print_new_sudoku(format="string", hints = HINT_NUMBER, logfile="generated_sudokus.txt", solution=False):  
    """Generates a new sudoku, logs it,
     and prints it in string or grid format, and the solution if selected."""
    generated_sudoku = generate(hints)

    if logfile:
        generated_sudoku.log_sudoku(logfile)

    print("Sudoku found:")
    if not format or format == "string":
        print(generated_sudoku.get_number_string())

    if not format or format == "grid":
        print(generated_sudoku)
    if solution:
        print(solve(generated_sudoku))



