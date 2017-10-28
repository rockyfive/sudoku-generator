# Sudoku generator 2015

import sudoku_solver as solver
import random
import time

HINT_NUMBER = 28

def initialize():
    sudoku = solver.Sudoku()
    box_list = list(sudoku.sudoku_list)
    random.shuffle(box_list)
    hints = range(1, 10)
    hints.pop(random.randrange(9))
    box = 0
    for number in range(HINT_NUMBER - 8):
        hints.append(random.randrange(1, 10))
    
    random.shuffle(hints)
    
    while hints and (box < len(box_list)):
        if (box_list[box].options > 1) and hints[0] in box_list[box].options:
            sudoku.play_idx(hints.pop(0), box_list[box].idx)

        box += 1
        
    return sudoku

def generate(extra_hints = 2):    
    new_sudoku = initialize()
    hints = extra_hints
    check_sudoku = solver.check(new_sudoku.clone())
    while check_sudoku and (check_sudoku != "Timeout"):
        if type(check_sudoku) == tuple:
            if not hints:
                return generate(extra_hints)
                
            new_sudoku.play_idx(check_sudoku[0], check_sudoku[1])
            check_sudoku = solver.check(new_sudoku.clone())
            hints -= 1
            continue
        return new_sudoku
        
    return generate(extra_hints)


def print_new_sudoku(format, hint_limit, solution=False):  
    initial_time = time.time()
    generated_sudoku = generate(hint_limit)
    print "Sudoku founded:"
    if format == "string":
        sudoku_str = ""
        for row in generated_sudoku.get_sudoku():
            for number in row:
                sudoku_str += str(number)
        print sudoku_str
    elif format == "draw":
        print generated_sudoku
    if solution:
        print solver.solution(generated_sudoku)
    print "Time elapsed in seconds:", time.time() - initial_time
        
     
print_new_sudoku("draw", 2, True)

