with open('sudoku.csv', 'r') as csvfile:
    sudokus = [{'sudoku': row[0], 'solution': row[1]} for row in
               [row.split(",") for row in csvfile]]

print(sudokus)
