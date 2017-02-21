assignments = []

cols = '123456789'
rows = 'ABCDEFGHI'

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [r + c for r in A for c in B]
    pass

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers
    twoVsBoxes = [box for box in values.keys() if len(values[box]) == 2]
    display(values)
    print("twoVsBoxes", twoVsBoxes)
    for box in twoVsBoxes:
        for box2 in twoVsBoxes:
            if box2 in peers[box] and values[box] == values[box2]:
                print(box, box2, values[box])
                digit1 = values[box][0]
                digit2 = values[box][1]

                for peerBox in peers[box]:
                    if (peerBox in peers[box2]) and len(values[peerBox]) > 1:
                        peerBoxV = values[peerBox]
                        print('br',peerBox, peerBoxV)
                        peerBoxV = peerBoxV.replace(digit1, '')
                        peerBoxV = peerBoxV.replace(digit2, '')
                        assign_value(values, peerBox, peerBoxV)
                        print('ar',peerBox, values[peerBox])

    print('after naked twins')
    display(values)
    reduce_puzzle(values)
    print('after reduce')
    display(values)
    search(values)
    print('after search')
    display(values)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    chars = []
    digits = '123456789'
    for c in grid:
        if c in digits:
            chars.append(c)
        if c == '.':
            chars.append(digits)
    assert len(chars) == 81
    return dict(zip(boxes, chars))
    pass

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print
    pass

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values
    pass

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                values[dplaces[0]] = digit
    return values
    pass

def reduce_puzzle(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

def search1(values):
    # "Using depth‐first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function     reduce_puzzle(values)
    # Choose one of the unfilled squares with the fewest possibilities
    if values is False:
        return False
    unsolved_values = [box for box in values.keys() if len(values[box]) > 1]

    if len(unsolved_values) == 0:
        return values   # solved
    else:
        sortedVK = sorted((len(values[box]), box) for box in unsolved_values)
        # sort all the unresolved boxes in acending order based on the length of
        # the value in the box                 

    # Starting from the first element in the list
    for i in range(0, len(sortedVK)):
        box = sortedVK[i][1]    # get the box key, which is the 2nd item
        for newV in values[box]:    # try for each possible value
            newValues = values.copy()   # copy the existing value
            newValues[box] = newV
            attempt = search(newValues)
            if attempt: # only if current branch resolves the puzzle
                return attempt  ### Even though the code cannot pass, but I think it's more Robost 
    pass

def search(values):
    # "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    pass

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
