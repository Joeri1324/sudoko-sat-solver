import subprocess
import re
import numpy
import SudokuIO as io

given_start = 1
given_end = 81
samples_num = 100

path = "/home/mas/Desktop/sudoko-sat-solver/100_hard_dataset/"
path_sol = "/home/mas/Desktop/sudoko-sat-solver/solversolution/"
stat_file = "/home/mas/Desktop/sudoko-sat-solver/solversolution/statistic.txt"
temp_file = "/home/mas/Desktop/sudoko-sat-solver/solversolution/temp.txt"


file = open(stat_file, "w")
file.write("%d\n%d\n" %(given_end-given_start, samples_num))
file.close()

for n in range(given_start, given_end):
    data = ""
    for i in range(samples_num):
        print("n,i:", n, i, '\n')
        readfile = path + str(n) + "/puzzle_" + str(i) + ".txt"
        solver_input = io.dataset_parse(readfile)

        io.save_list_in_file(temp_file, solver_input)

        proc = subprocess.Popen(["python", "-c", "import SudokuSolver as ss;"
                                         "import SudokuIO as io;"
                                         "file = open('/home/mas/Desktop/sudoko-sat-solver/solversolution/temp.txt', "r");"
                                         "sudoku = [[x] for x in io.file_to_list(file)];"
                                         "file.close();"
                                         "solver = ss.SudokuSolver(); "
                                         "solver.solve(sudoku);"],stdout=subprocess.PIPE)
        current = str(proc.communicate()[0])
        current = re.sub("\\\\n", '\n', current)
        data += current + "\n"
    file = open(stat_file, "a")
    file.write(data+"\n")
    file.write("=========================================\n")
    file.close()

