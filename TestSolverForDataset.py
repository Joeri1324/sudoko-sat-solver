import SudokuIO as io		
import time		
import os		
import SudokuSolver

given_start = 1
given_end = 81
samples_num = 100

path = "/home/mas/Desktop/sudoko-sat-solver/100_hard_dataset/"
path_sol = "/home/mas/Desktop/sudoko-sat-solver/solversolution/"		
path_converted_sol = "/home/mas/Desktop/sudoko-sat-solver/solversolution/convertedsol/"				

solver = SudokuSolver()
for n in range(given_start, given_end):
    for i in range(samples_num):
        #define pathes for reading from dataset and writing to the files:		
	if not os.path.exists(path + str(n) + "/"):		
	os.mkdir(path + str(n))		
	if not os.path.exists(path_sol + str(n) + "/"):		
	os.mkdir(path_sol + str(n))		
	if not os.path.exists(path_converted_sol + str(n) + "/"):		
	os.mkdir(path_converted_sol + str(n))		

	readfile = path + str(n) + "/puzzle_" + str(i) + ".txt"		
	writefile = path_sol + str(n) + "/sat_solution_" + str(i) + ".txt"		
	converted_sol = path_converted_sol + str(n) + "/index_free_sol_" + str(i) + ".txt"		

	#convert the normal input from data set to a readable form for sat solver:		
	solver_input = io.dataset_parse(readfile)		

	#solving evey puzzle:				
	solution = solver.solve(solver_input)		

	#saving our predicted solutions to file		
	io.save_solution(writefile, solution)		
	io.save_solution_without_index(converted_sol, solution)


