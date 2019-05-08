# Sudoku generator 2015

from sudoku_solver import solve
from sudoku import Sudoku
import random
import time

HINT_NUMBER = 27

EXTRA_HINTS = 3

LOGFILE = "generated_sudokus.txt"

def initialize_random_sudoku(hint_number):
    sudoku = Sudoku()
    box_list = list(sudoku.sudoku_list)
    random.shuffle(box_list)

    hints = list(range(1, 10))
    hints.pop(random.randrange(9))
    box = 0
    for number in range(hint_number - 8):
        hints.append(random.randrange(1, 10))
    
    random.shuffle(hints)
    
    while hints and (box < len(box_list)):
        if (len(box_list[box].possible_values) > 1) and hints[0] in box_list[box].possible_values:
            sudoku.play_idx(hints.pop(0), box_list[box].idx)

        box += 1
        
    return sudoku

def generate(hint_number, extra_hints):    
    new_sudoku = initialize_random_sudoku(hint_number)
    check_sudoku = solve(new_sudoku.clone(), True)
    while check_sudoku and (check_sudoku != "Timeout"):
        if type(check_sudoku) == tuple:
            if not extra_hints:
                return generate(hint_number, extra_hints)
                
            new_sudoku.play_idx(check_sudoku[0], check_sudoku[1])
            check_sudoku = solve(new_sudoku.clone(), True)
            hint_number -= 1
            continue
        return new_sudoku
        
    return generate(hint_number, extra_hints)


def print_new_sudoku(format="string", hint_number = HINT_NUMBER, extra_hints=EXTRA_HINTS, logfile=LOGFILE, solution=False):  
    """Generates a new sudoku, logs it,
     and prints it in string or grid format, and the solution if selected."""
    generated_sudoku = generate(hint_number, extra_hints)

    if logfile:
        generated_sudoku.log_sudoku(logfile)

    print("Sudoku found:")
    if not format or format == "string":
        print(generated_sudoku.get_number_string())

    if not format or format == "grid":
        print(generated_sudoku)
    if solution:
        print(solve(generated_sudoku))



