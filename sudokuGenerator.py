#Square matrix. Default 9x9
import copy
import random
import time

gridSize = 9
maxStackDepth = 80  #Some random grid combinations won't work or will take to long to generate. Cap so we don't try forever with these.
blankSquares = 30 #runs into issues when we have more than about 43 blank squares

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

    #check row
    if number in grid[row]: return False

    # column. len(line) will be whatever we've generated up to (e.g. 7 columns into the grid)
    for _row in grid:
        if _row[row_index] == number:
            return False

    #Get our 3x3 square relative to our current position and check if the number is in any of those squares.
    #Top left corner will always be how many indexes past row % 3 we are (0 if we're in the first row of a 3x3 square) and same for column
    #e.g. if we're at row 8 column 4 (starting from 0) -> 7 % 3 = 1, 3 % 3 = 0, so the square starts at 6, 3 or row 7 column 4
    #TODO: simplify is_number_valid to work like this but only up to the selected row[row_index]

    corner_row = row - row % 3
    corner_col = row_index - row_index % 3

    #We know our grid is fully generated so just check every square in the grid
    for i in range(3):
        for j in range(3):
            if grid[corner_row + i][corner_col + j] == number:
                return False
    return True


#print the grid as an array so we can easily copy it over to the solver
def printBlankedGrid(grid):
    # python assignment doesn't make a new copy, just shares a reference, so we need a deep copy to not manipulate original grid.
    array_grid = copy.deepcopy(grid)

    for i in range(gridSize):
        for j in range(gridSize):
            if array_grid[i][j] == ' ':
                array_grid[i][j] = 0

    print(array_grid)


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
def remove_spaces(grid, depth = 0):

    if depth == maxStackDepth:
        print("\nTimeout reached. Could not generate puzzle. Try again with fewer blank spaces or a larger MaxStackDepth.")
        return

    blanked_grid = copy.deepcopy(grid)
    grid_coordinates = generate_grid_coordinates()
    random.shuffle(grid_coordinates)

    #We want to keep track of how many times we've tried blanking the current grid. If we exceed a certain amount,
    #dump the blanked_grid and try again.
    repeat_counter = 0
    num_blanks = 0

    while num_blanks < blankSquares:
        #if we've gone through everything already, try a few more times
        if len(grid_coordinates) == 0:
            if repeat_counter < maxStackDepth:
                grid_coordinates = generate_grid_coordinates()
                random.shuffle(grid_coordinates)
                repeat_counter += 1
            #We weren't able to finish the current blanked grid. Dump it and try a new one
            else:
                if depth % 5 == 0:
                    print("\nGenerating blank spaces...")
                return remove_spaces(grid, depth + 1)

        x, y = grid_coordinates[0]

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

    print('\n Puzzle generated!')
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

    return grid


#recursively goes through the grid possibilities until we hit a solution using backtracking.
def solve(grid, row = 0, col = 0):
    #last column. If we're at the last row, we solved it and are done otherwise move to the next row
    if col == 9:
        if row == 8:
            return True

        row += 1
        col = 0

    #number already filled. move on to the next one
    if grid[row][col] > 0:
        return solve(grid, row, col + 1)

    #other columns. See if there's a valid move. If so move on to the next, if not set it to 0 and iterate
    for number in range(1, 10):
        if is_number_possible(grid, number, row, col):
            grid[row][col] = number

            if solve(grid, row, col + 1):
                return True

        grid[row][col] = 0

    #We hit a dead end, go back
    return False


def mainMenu(choice=0, grid=None):

    if choice <= 0:
        print("\n***************************MAIN MENU********************************\n"
              "\nPress 1 to generate a grid, 2 to solve a generated grid. 3 to exit")
        choice = int(input())

    if choice == 1:
        if grid == None:
            grid = generate()
            print("Grid complete!")

        print("\n********************************************************************\n"
              "Press 1 to pretty print the grid, 2 to turn it into a new puzzle. 3 to go back to main menu.")
        choice = int(input())

        match choice:
            case 1:
                pretty_Print(grid)
                mainMenu(1, grid)

            case 2:
                puzzle_grid = remove_spaces(grid)
                if puzzle_grid:
                    print("***********************************************************\n"
                          "Press 1 to pretty print the puzzle grid, 2 to print it as an array for the solver.")
                    choice = int(input())
                    match choice:
                        case 1: pretty_Print(puzzle_grid)
                        case 2: printBlankedGrid(puzzle_grid)
                    mainMenu(1, grid)

            case 3: mainMenu(0, grid)

    elif choice == 2:
        print("Pass in a grid in the following format: '[[1,2,3,0,0,6,7,8,9], [row2], [row3], ..., [row9]]' where 0 is a blank space. Use the generator for an example")
        _grid = eval(input())
        print(_grid)
        if solve(_grid):
            print("Solved grid:")
            pretty_Print(_grid)
            mainMenu(0)
        else:
            print("Could not solve grid.\n")

        mainMenu()

    elif choice == 3:
        exit()


mainMenu()


