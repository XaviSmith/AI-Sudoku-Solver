#Square matrix. Default 9x9
import copy
import random
import time

gridSize = 9
maxStackDepth = 20  #Some random grid combinations won't work or will take to long to generate. Cap so we don't try forever with these.
blankSquares = 40

#e.g. check(from row2, index3, for 9 in, y + delta_y1, y + delta_y2)
def check_neighbouring_cells(row, row_index, number, delta1, delta2):
    return row[row_index + delta1] == number or row[row_index + delta2] == number

#checks if number is in  relative_row.
#e.g. check(matrix for 5, in -1 rows from us, from index 6)
def is_number_in_relative_row(grid, number, relative_row, row_index):
    _row = grid[relative_row]

    #numbers to check relative to our number
    #e.g. index 2 + 1, index 2 + 2, then we check index 2 - 1, index 2 + 0
    delta1 = 1
    delta2 = 2

    #check numbers in the row from left to right, changing deltas as we go to 1,2  -1,1, -2,-1, -3-2,
    for i in range(3):
        #if we're checking ourself (row_index + 3 so that we don't get <0 for first row when checking (row_index-i) % 3 == 0 (ourself)
        if (row_index + 3 - i) % 3 == 0:
            if check_neighbouring_cells(_row, row_index, number, delta1, delta2):
                return True

        if i == 0:
            delta1 -= 2
            delta2 -= 1

        elif i == 1:
            delta1 -= 1
            delta2 -= 2

        else:
            delta1 -= 1
            delta2 -= 1

    return False


#A number is valid if: it's not already in the row, column, or same grid square
def is_number_valid(grid, line, number):
    #check if number is in our row
    if number in line:
        return False
    #column. len(line) will be whatever we've generated up to (e.g. 7 columns into the grid)
    for row in grid:
        if row[len(line)] == number:
            return False

    #check if it's in our 3x3 square (not necessary if we've only built out the first row since there'd be nothing to check)
    #if we're in the 2nd row of the 3x3 square.
    # The row is only appended after to the grid after the fact so len(grid) is how many rows are above us
    if len(grid) % 3 == 1:
        # if previous line didn't have this number
        return not is_number_in_relative_row(grid, number, -1, len(line))
        # if we're in the 3rd row of the 3x3 square
    if len(grid) % 3 == 2:
        # if the previous line and line before don't have this number
        return not (is_number_in_relative_row(grid, number, -1, len(line)) or is_number_in_relative_row(grid, number,
                                                                                                        -2, len(line)))

    return True

#Same as above, but with a finished grid
def is_number_possible(grid, number, row, row_index):
    if number in grid[row]: return False

    for _row in grid:
        if _row[row_index] == number: return False

    if row % 3 == 1:
        #2nd row of square
        return not is_number_in_relative_row(grid, number, -1, row_index)
    if row % 3 == 2:
        #3rd row of square
        return not (is_number_in_relative_row(grid, number, -1, row_index) or
                    is_number_in_relative_row(grid, number, -2, row_index))
    return True

def pretty_Print(grid):
    print("Puzzle:")
    # enumerate is the python i++
    for r, row in enumerate(grid):
        puzzle = ""
        for c, column in enumerate(row):
            puzzle += " {} ".format(column)
            #Separator TODO: rewrite this to work with diff grid sizes
            if(c + 1) % 3 == 0 and (c + 1) != gridSize:
                puzzle += "|"
        print(puzzle)
        #Separator
        if(r + 1) % 3 == 0 and (r + 1) != gridSize:
            print("-" * ( (gridSize * 3) + 2))

#Generates a list of coordinates for the grid (e.g. [ [0,0], [0,1] ... [9,9] ])
#TODO: Generate coordinates while generating the grid
def generate_grid_coordinates():
    result = []

    for i in range(gridSize):
        for j in range(gridSize):
            result.append([i, j])

    return result

#Essentially we get random parts of the grid one at a time, blank out the square, and see if only 1 number is possible in that square
#Repeat until we have the specified blankSquares
def remove_spaces(grid):
    #python assignment doesn't make a new copy, just shares a reference, so we need a deep copy to not manipulate original grid.
    blanked_grid = copy.deepcopy(grid)
    grid_coordinates = generate_grid_coordinates()
    random.shuffle(grid_coordinates)

    #We want to keep track of how many times we've tried blanking the current grid. If we exceed a certain amount,
    repeat_counter = 0
    num_blanks = 0

    while num_blanks < blankSquares:

        #if we're on a repeat and the grid spot is already blanked, skip it.
        if blanked_grid[x][y] == ' ':
            del grid_coordinates[0]
            continue

        #Check if multiple numbers are possible in the selected coordinates
        possible_numbers = 0
        for i in range(1, gridSize + 1):
            #blank out the number so we can check the possibilities afterward
            num_to_check = blanked_grid[x][y]
            blanked_grid[x][y] = ' '

            if is_number_possible(blanked_grid, i, x, y):
                possible_numbers += 1

            blanked_grid[x][y] = num_to_check

        #if there's only one possible number in that spot blank it out, otherwise try with a different coordinate
        if possible_numbers == 1:
            blanked_grid[x][y] = ' '
            num_blanks += 1
            repeat_counter = 0
            del grid_coordinates[0]
        else:
            del grid_coordinates[0]

    return blanked_grid




def generate(depth = 0):
    if depth == maxStackDepth:
        print("MAX STACK DEPTH REACHED. TRY AGAIN")
        return

    grid = []
    #so we don't spend too long trying to generate a puzzle that just wouldn't work
    start_time = time.time()
    numbers = list(range(1, gridSize + 1))
    #row
    for i in range(gridSize):
        new_row = []
        #individual column within row
        while len(new_row) < gridSize:
            _number = random.choice(numbers)

            #keep track of the numbers we tried. If we tried all 9 and they're not valid we made something unsolvable, try again
            repeat_counter = 0
            while not is_number_valid(grid, new_row, _number):
                _number = random.choice(numbers)
                repeat_counter += 1
                if repeat_counter == gridSize:
                    new_row = []
                    break
                if time.time() - start_time > 0.3: #we're taking too long and likely ran into a problem. Dump the grid and try again
                    generate(depth + 1)
                    return

            #python has a while else clause that only happens when the while loop isn't broken out of
            else:
                new_row.append(_number)

        grid.append(new_row)
    pretty_Print(grid)
    puzzle_grid = remove_spaces(grid)
    print("\n")
    pretty_Print(puzzle_grid)

generate()
