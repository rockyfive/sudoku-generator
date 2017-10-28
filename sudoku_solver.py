# Sudoku solver 2015

import time

class Sudoku:
    """ Class that represents the sudoku. """
    def __init__(self, sudoku=False):
        #self.sudoku = sudoku # initial 2D array.
        self.sudoku_grid = [[Box(self, row, col) for col in xrange(9)] for row in xrange(9)]
        self.rows = [Section(row) for row in self.sudoku_grid]
        self.cols = [Section([self.sudoku_grid[row][col] for row in xrange(9)]) for col in xrange(9)]
        self.squares = [Section([self.sudoku_grid[((idx / 3) * 3) + (pos / 3)][((idx % 3) * 3) + (pos % 3)] for pos in xrange(9)])
                        for idx in xrange(9)]
        self.sections = self.rows + self.cols + self.squares
        self.sudoku_list = [self.sudoku_grid[row][col] for row in xrange(9) for col in xrange(9)]
        self.index_list = range(81)
        if sudoku:
            for row in xrange(9): # Here we fill the initial values.
                for col in xrange(9):
                    if sudoku[col][row]:
                        self.play_pos(sudoku[col][row], (col, row))
        
    def __str__(self):
        self.rep = "" # String representation saved here.
        for row in xrange(9):
            if not row % 3 and row:
                self.rep += "------+-------+------\n"
            self.rep += self.rows[row].__str__()
            self.rep += "\n"
        return self.rep
    
    def get_sudoku(self):
        """ Returns a 2D array with the values. """
        return [[self.sudoku_grid[row][col].value for col in xrange(9)] for row in xrange(9)]
    
    def delete(self, value, row, col, square):
        """ This function is called when a number is played. """
        self.rows[row].delete(value)
        self.cols[col].delete(value)
        self.squares[square].delete(value)
        
    def play_pos(self, value, pos):
        """ Plays value on the position. """
        self.sudoku_grid[pos[0]][pos[1]].set_value(value)
        
    def play_idx(self, value, index):
        """ Plays value on the index. """
        self.sudoku_list[index].set_value(value)
        
    def clone(self):
        """ Returns a clone of the sudoku. """
        return Sudoku(self.get_sudoku())
        
        
class Box:
    """ Class that reprents a position in the sudoku. """
    
    def __init__(self, sudoku, row, col):
        self.value = 0 # Actual value
        self.options = [1, 2, 3, 4, 5, 6, 7, 8, 9] # Possible values
        self.row = row
        self.col = col
        self.square = (col / 3) + (row / 3) * 3
        self.sudoku = sudoku 
        self.idx = (col) + (row * 9) # index of the box.
      
    def __str__(self):
        if not self.value:
            return "_"
        else:
            return str(self.value)
        
    def delete(self, number):
        """ Delete a number from options list. """
        if number in self.options:
            self.options.remove(number)
    
    def set_value(self, value):
        """ Changes the value of the box. """
        # Sets the value
        self.value = value 
        # Being the box occupied, delete the other numbers as option.
        self.options = [] 
        # Delete the value as option for other boxes on the same sections.
        self.sudoku.delete(value, self.row, self.col, self.square) 
        # Remove the box on the index list of free boxes.
        self.sudoku.index_list.remove(self.idx)
        
        # With the next code is taken in account that
        # on the sections of the boxes that shares a section
        # with this box, the value played in this box is not
        # going in that boxes.
        for section in [self.sudoku.rows[self.row], self.sudoku.cols[self.col], self.sudoku.squares[self.square]]:
            for key, item in section.numbers.items():
                try: # We remove this box as option, because it's filled.
                    item.remove(self.idx)
                except:
                    pass
            for box in section.boxes:
                for lsection in [box.sudoku.rows[box.row], box.sudoku.cols[box.col], box.sudoku.squares[box.square]]:
                    # for the sections related, for the value played in this box, 
                    # we remove that section's boxes as an option.
                    try: 
                        lsection.numbers[value].remove(box.idx)
                    except:
                        pass

                    
class Section:
    """ Represents rows, cols and squares. """
    def __init__(self, boxes):
        self.boxes = boxes # list of box objects contained in the section.
        # Dictionary with 1-9 numbers as keys and a list with possible boxes' index as value.
        self.numbers = dict((key, [box.idx for box in self.boxes]) for key in xrange(1, 10))
    def __str__(self):
        self.rep = "" # String representation saved here.
        for box in self.boxes:
            if not box.idx % 3 and box.idx % 9:
                self.rep += "| "
            self.rep += box.__str__() + " "
        return self.rep
    
    def delete(self, value):
        """ Delete a value on the options of the boxes of the section. """
        self.numbers.pop(value, None)
        for box in self.boxes:
            box.delete(value)

# main functions

def solution(sudoku):
    """ Returns a solution of the sudoku,
    or None if doesn't have any solution. """
    return solve(sudoku, time.time())

def check(sudoku):
    """ Checks if the sudoku has only one solution,
    if not, returns a value and an index box. """
    return solve(sudoku, time.time(), True)
    
    
# Helper functions

def solve(sudoku, start_time, check = False):
    """ Tries to solve the sudoku. """
    # We set a maximum depth to avoid an infinite loop.
    if (time.time() - start_time) > 10.0:
        return "Timeout"

    sudoku_after = sudoku.get_sudoku()
    sudoku_before = sudoku_00
    # Tries to fill the sudoku until no more boxes can be filled.
    while(sudoku_after != sudoku_before):
        sudoku_before = sudoku_after
        unique_candidate(sudoku)
        sole_candidate(sudoku)
        sudoku_after = sudoku.get_sudoku()
        
    if not sudoku.index_list: # checks if all boxes are filled.
        return sudoku
    # The next code iterates all boxes looking for one of
    # the boxes with less options available.
    next_play = 81 
    options_length = 10
    for box in list(sudoku.sudoku_list): 
        if box.options and len(box.options) < options_length:
            next_play = box.idx
            options_length = len(box.options)
    # If there is no box to be filled and no solution we exit the function.
    if next_play == 81:
        return False
    # Now we iterate over the box's options we have chosen before
    # and try them in other instance of the sudoku in a recursive way.
    solved = False
    result = 0
    for option in sudoku.sudoku_list[next_play].options:
        next_sudoku = sudoku.clone()
        next_sudoku.play_idx(option, next_play)
        solution = solve(next_sudoku, start_time, check)

        if solution:
            if solution == "Timeout":
                return "Timeout" # Once a solution is found, the function returns it.
            if not check:
                return solution
            if solved:
                return (option, next_play)
            else:
                solved = True
                result = solution
    if solved:           
        return result
        # If there is no solution, the function will just finish
        # and it'll return the default value None. Other return
        # value can be added here at the end.
    

def sole_candidate(sudoku):
    """ Solving method searching a sole candidate
        for a box. """
    state = 1
    while state:
        state = 0
        for idx in sudoku.index_list:
            if len(sudoku.sudoku_list[idx].options) == 1:
                sudoku.play_idx(sudoku.sudoku_list[idx].options[0], idx)
                state = 1
                
def unique_candidate(sudoku):
    """ Solving method searching a unique box
        candidate for a number in a section. """
    state = 1
    while state:
        state = 0
        for section in sudoku.sections:
            for number, boxes in section.numbers.items():
                if len(boxes) == 1:
                    sudoku.play_idx(number, boxes[0])
                    state = 1

                    
sudoku_00 = [[0, 0, 0, 0, 0, 0, 0, 0, 0], # needed to solve function.
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0 ,0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0, 0, 0, 0, 0]]

sudoku_99 = [[8, 0, 0, 0, 0, 0, 0, 0, 0],
             [0, 0, 3, 6, 0, 0, 0, 0, 0],
             [0, 7, 0, 0, 9, 0, 2, 0 ,0],
             [0, 5, 0, 0, 0, 7, 0, 0, 0],
             [0, 0, 0, 0, 4, 5, 7, 0, 0],
             [0, 0, 0, 1, 0, 0, 0, 3, 0],
             [0, 0, 1, 0, 0, 0, 0, 6, 8],
             [0, 0, 8, 5, 0, 0, 0, 1, 0],
             [0, 9, 0, 0, 0, 0, 4, 0, 0]]

      
#test = Sudoku(sudoku_99)

#print check(test)
