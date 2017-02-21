from utils import *

assignments = []

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
    stalled = False # Initilize the stalled value for looping
    while not stalled:
        # Idenify the boxes with 2 values
        twoVsBoxes = [box for box in values.keys() if len(values[box]) == 2]

        # Copy the value of current values dictionary, need to use copy() function
        old_values = values.copy()
        for box in twoVsBoxes:
            for box2 in twoVsBoxes:
                # In the nested loop, only proceed when the 2 chosen boxes are in
                # the same unit. And the box values are the same, this is naked twins
                if box2 in peers[box] and values[box] == values[box2]:
                    digit1 = values[box][0]
                    digit2 = values[box][1]

                    # Find the 3rd box from the same unit. It has to be the peer
                    # of box and box2
                    for peerBox in peers[box]:
                        if (peerBox in peers[box2]) and len(values[peerBox]) > 1:
                            peerBoxV = values[peerBox]
                            peerBoxV = peerBoxV.replace(digit1, '')
                            peerBoxV = peerBoxV.replace(digit2, '')
                            values = assign_value(values, peerBox, peerBoxV)

        if old_values == values:    # If one loop doesn't change anything
            stalled = True

    return values   # Must return values for assertion test

# Nothing different than previous function, except diagonal rule
def diag_naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers    
    stalled = False # Initilize the stalled value for looping
    while not stalled:
        # Idenify the boxes with 2 values
        twoVsBoxes = [box for box in values.keys() if len(values[box]) == 2]

        # Copy the value of current values dictionary, need to use copy() function
        old_values = values.copy()
        for box in twoVsBoxes:
            for box2 in twoVsBoxes:
                # In the nested loop, only proceed when the 2 chosen boxes are in
                # the same unit. And the box values are the same, this is naked twins
                if box2 in diagpeers[box] and values[box] == values[box2]:
                    digit1 = values[box][0]
                    digit2 = values[box][1]

                    # Find the 3rd box from the same unit. It has to be the peer
                    # of box and box2
                    for peerBox in diagpeers[box]:
                        if (peerBox in diagpeers[box2]) and len(values[peerBox]) > 1:
                            peerBoxV = values[peerBox]
                            peerBoxV = peerBoxV.replace(digit1, '')
                            peerBoxV = peerBoxV.replace(digit2, '')
                            values = assign_value(values, peerBox, peerBoxV)

        if old_values == values:    # If one loop doesn't change anything
            stalled = True

    return values   # Must return values for assertion test

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
    """
    Eliminate the values from a box if its peers have determined value
    Args:
        values(dict): The sudoku in dictionary form
    Retursn:
        values(dict): The sudoku in dictionary form after the elimination
    """
    # Find the solved boxes, which are with only 1 value
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]: # Eliminate this value from all its peers
            values = assign_value(values, peer, values[peer].replace(digit,''))
    return values
    pass

# Nothing different than previous function, except diagonal rule
def diag_eliminate(values):
    """
    Eliminate the values from a box if its peers have determined value
    Args:
        values(dict): The sudoku in dictionary form
    Retursn:
        values(dict): The sudoku in dictionary form after the elimination
    """
    # Find the solved boxes, which are with only 1 value
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for diagpeer in diagpeers[box]:
            values = assign_value(values, diagpeer, values[diagpeer].replace(digit,''))
    return values
    pass

def only_choice(values):
    """
    If a box has multiple values, but for one specific value all its peers in the same unit
    don't have it. Then the specific value will be assign to this box.
    Args:
        values(dict): The sudoku in dictionary form
    Retursn:
        values(dict): The sudoku in dictionary form after the only_choice
    """
    for unit in unitlist:   # For every unit (9 boxes)
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                # If a digit appears only once in the boxes of 1 unit
                values = assign_value(values, dplaces[0], digit)
    return values
    pass

# Nothing different than previous function, except diagonal rule
def diag_only_choice(values):
    """
    If a box has multiple values, but for one specific value all its peers in the same unit
    don't have it. Then the specific value will be assign to this box.
    Args:
        values(dict): The sudoku in dictionary form
    Retursn:
        values(dict): The sudoku in dictionary form after the only_choice
    """
    for diagunit in diagunitlist:
        for digit in '123456789':
            dplaces = [box for box in diagunit if digit in values[box]]
            if len(dplaces) == 1:
                values = assign_value(values, dplaces[0], digit)
    return values
    pass

def reduce_puzzle(values):
    # Use a while loop to apply eliminate and only_choice iteratively until no change
    stalled = False
    while not stalled:
        # Count the number of solved boxes whoes value length is 1
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        # Count the number of solved boxes whoes value length is 1
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If before and after count is the same, meaning no change, return
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

# Nothing different than previous function, except diagonal rule
def diag_reduce_puzzle(values):
    stalled = False
    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = diag_eliminate(values)
        values = diag_only_choice(values)
        values = diag_naked_twins(values)
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values
    pass

def search1(values):
    """
    My alternative search function which I think it's more sophisticated
    """
    # Apply the reduce_puzzle first
    values = reduce_puzzle(values)
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
            new_sudoku = values.copy()   # copy the existing value
            new_sudoku = assign_value(new_sudoku, box, newV)
            attempt = search(new_sudoku)
            if attempt: # only if current branch resolves the puzzle
                return attempt  ### Even though the code cannot pass, but I think it's more Robost 
    pass

def diag_search1(values):
    """
    My alternative search function which I think it's more sophisticated
    """
    values = diag_reduce_puzzle(values)
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
            new_sudoku = values.copy()   # copy the existing value
            new_sudoku = assign_value(new_sudoku, box, newV)
            attempt = diag_search1(new_sudoku)
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
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt = search(new_sudoku)
        if attempt:
            return attempt
    pass

# Nothing different than previous function, except diagonal rule
def diag_search(values):
    # "Using depth-first search and propagation, try all possible values."
    # First, reduce the puzzle using the previous function
    values = diag_reduce_puzzle(values)
    #display(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    # Now use recurrence to solve each one of the resulting sudokus, and 
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku = assign_value(new_sudoku, s, value)
        attempt = diag_search(new_sudoku)
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
    values_dict = grid_values(grid)
    return diag_search1(values_dict)
    pass

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
