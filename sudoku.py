class Sudoku:
    """ Class that represents the sudoku. """
    def __init__(self, sudoku=False, empty_value="0"):
        self.sudoku_grid = [[Box(self, row, col) for col in range(9)] for row in range(9)]
        self.rows = [Section(row) for row in self.sudoku_grid]
        self.cols = [Section([self.sudoku_grid[row][col] for row in range(9)]) for col in range(9)]
        self.squares = [Section([self.sudoku_grid[((idx // 3) * 3) + (pos // 3)][((idx % 3) * 3) + (pos % 3)] for pos in range(9)])
                        for idx in range(9)]
        self.sections = self.rows + self.cols + self.squares
        self.sudoku_list = [self.sudoku_grid[row][col] for row in range(9) for col in range(9)]
        self.index_list = list(range(81))

        if type(sudoku) == list:
            for row in range(9): 
                for col in range(9):
                    if sudoku[col][row]:
                        self.play_pos(sudoku[col][row], (col, row))

        if type(sudoku) == str:
            for index in self.index_list:
                if sudoku[index] != empty_value:
                    self.play_idx(sudoku[index], index)


    def __str__(self):
        self.rep = "" # String representation saved here.
        for row in range(9):
            if not row % 3 and row:
                self.rep += "------+-------+------\n"
            self.rep += self.rows[row].__str__()
            self.rep += "\n"
        return self.rep
    
    def get_sudoku(self):
        """ Returns a 2D array with the values. """
        return [[self.sudoku_grid[row][col].value for col in range(9)] for row in range(9)]

    def get_number_string(self):
        """ Returns the sudoku as a string of numbers. """
        sudoku_str = ""
        for row in self.get_sudoku():
            for number in row:
                sudoku_str += str(number)
        return sudoku_str
    
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

    def clone_and_play(self, value, index):
        new_sudoku = self.clone()
        new_sudoku.play_idx(value, index)
        return new_sudoku
        
    def log_sudoku(self, logfile):
        f = open(logfile, "a")
        f.write(self.get_number_string() + "\n")
        f.close()
        
class Box:
    """ Class that reprents a position in the sudoku. 
    Tracks the possible legal values if not filled. """
    
    def __init__(self, sudoku, row, col):
        self.value = 0 # Actual value
        self.options = [1, 2, 3, 4, 5, 6, 7, 8, 9] # Possible values
        self.row = row
        self.col = col
        self.square = (col // 3) + (row // 3) * 3
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
        """ Changes the value of the box."""
        self.value = value 
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
            for key, item in list(section.numbers.items()):
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
        self.numbers = dict((key, [box.idx for box in self.boxes]) for key in range(1, 10))
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