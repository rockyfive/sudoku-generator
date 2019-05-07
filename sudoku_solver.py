# Sudoku solver 2015

from time import time
from sudoku import Sudoku


TIMEOUT = 10.0
# main functions

def solve(sudoku, check_unique_solution = False):
    """ Tries to solve the sudoku. """

    def inner_solve(sudoku, start_time):
        # We set a maximum timeout.
        if (time() - start_time) > TIMEOUT:
            return "Timeout"

        fill_easy_positions(sudoku)
            
        if not sudoku.empty_boxes: # checks if all boxes are filled.
            return sudoku

        next_play = find_box_with_less_possible_values(sudoku)
    
        if next_play == len(sudoku.sudoku_list):
            return False
        # Now we iterate over the box's possible_values we have chosen before
        # and try them in other instance of the sudoku in a recursive way.
        result = None
        solved = False
        for option in sudoku.sudoku_list[next_play].possible_values:

            next_sudoku = sudoku.clone_and_play(option, next_play)
            solution = inner_solve(next_sudoku, start_time)

            if solution:
                if solution == "Timeout":
                    return "Timeout" # Once a solution is found, the function returns it.
                if not check_unique_solution:
                    return solution
                if solved:
                    return (option, next_play)
                else:
                    solved = True
                    result = solution

        if solved:
            return result
        return None
        
    return inner_solve(sudoku, time())
    
    
# Helper functions

def fill_easy_positions(sudoku):
    """Tries to fill the sudoku until no more boxes can be filled
     with sole_candidate and unique_candidate methods."""
    sudoku_after = sudoku.get_sudoku()
    sudoku_before = None
    while(sudoku_after != sudoku_before):
        sudoku_before = sudoku_after
        unique_candidate(sudoku)
        sole_candidate(sudoku)
        sudoku_after = sudoku.get_sudoku()

def find_box_with_less_possible_values(sudoku):
    """Iterates all boxes looking for 
    the first box with less possible_values available."""
    result = len(sudoku.sudoku_list)
    min_length = 10
    for box in list(sudoku.sudoku_list): 
        if box.possible_values and len(box.possible_values) < min_length:
            result = box.idx
            min_length = len(box.possible_values)
    return result   

def sole_candidate(sudoku):
    """ Solving method searching a sole candidate
        for a box. """
    state = 1
    while state:
        state = 0
        for idx in sudoku.empty_boxes:
            if len(sudoku.sudoku_list[idx].possible_values) == 1:
                sudoku.play_idx(sudoku.sudoku_list[idx].possible_values[0], idx)
                state = 1
                
def unique_candidate(sudoku):
    """ Solving method searching a unique box
        candidate for a number in a section. """
    state = 1
    while state:
        state = 0
        for section in sudoku.sections:
            for number, boxes in list(section.numbers.items()):
                if len(boxes) == 1:
                    sudoku.play_idx(number, boxes[0])
                    state = 1
