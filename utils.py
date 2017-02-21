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

"""
diag_units1 = []
diag_units2 = []
for i in range(0, 9):
    diag_units1.append([cross(r, c) for r in rows[i] for c in cols[i]][0][0])
    diag_units2.append([cross(r, c) for r in rows[8-i] for c in cols[i]][0][0])
diag_units = [diag_units1, diag_units2]
"""

diag_units0 = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]

diagunitlist = unitlist + diag_units0
diagunits = dict((s, [u for u in diagunitlist if s in u]) for s in boxes)
diagpeers = dict((s, set(sum(diagunits[s],[]))-set([s])) for s in boxes)
