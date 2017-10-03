from SudokuSolver import SudokuSolver
import os
import json


solver = SudokuSolver()
rules = solver.get_rules(9)
probs = []
for i in range(1, 81):
    folder = 'data/' + str(i) + '/' 
    total = 100
    counter = 0
    for filename in os.listdir(folder):    
        if 'puzzle' in filename:
            counter += 1 if solver.is_proper(solver.sudoku_to_cnf(folder + filename) + rules) else 0
    prob = counter/total
    probs.append({'givens': i, 'prob': prob})


with open('properness_probs.json', 'w') as fp:
    json.dump({'data': probs}, fp)