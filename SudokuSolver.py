import itertools
import sys
import math
import pycosat
import os
import time
import SudokuIO

class SudokuSolver(object):

    def strip(self, x, y, number):
        """
        strip returns the negative value of x, y and number appended.
        """
        return int('-' + str(int(x)) + str(int(y)) + str(number))

    def get_unaryrules(self, index, M):
        """
        get_unaryrules returns the rules that make sure in one square
        there can be only one number for index.
        """
        return list(
            itertools.chain.from_iterable(
                [[[y, self.strip(index[0], index[1], x)] for x in range(1, M+1)
                  if y != self.strip(index[0], index[1], x)] for y in
                 [self.strip(index[0], index[1], i) for i in range(1, M+1)]]
            ))

    def at_least_one_rules(self, index, M):
        """
        at_least_one_rule returns the rules that make sure there has
        to be at least one number in a square.
        """
        return [[int(str(index[0]) + str(index[1]) + str(x))
                for x in range(1, M+1)]]

    def get_rowrules(self, index, M):
        """
        get_rowrules returns the rules that make sure no duplicates can
        be in one row.
        """
        return list(itertools.chain.from_iterable(
            [[[self.strip(index[0], index[1], i), self.strip(x, index[1], i)]
              for x in range(1, M+1) if x != index[0]]
                for i in range(1, M+1)]
        ))

    def get_columnrules(self, index, M):
        """
        get_columnrules returns the rules that make sure no duplicated can
        be in a column.
        """
        return list(itertools.chain.from_iterable(
            [[[self.strip(index[0], index[1], i), self.strip(index[0], x, i)]
              for x in range(1, M+1) if x != index[1]]
                for i in range(1, M+1)]
        ))

    def lower_index(self, x, index, M):
        """
        lower_index returns the index warped down to the bottom left square of
        the square index is in.
        """
        return [x[0]+index[0]-((index[0]-1) % math.sqrt(M)),
                x[1]+index[1]-((index[1]-1) % math.sqrt(M))]

    def get_boxrules(self, index, M):
        """
        get_boxrules returns the rules that make sure there can be no
        duplicates in one box.
        """
        return list(itertools.chain.from_iterable(
            [[[self.strip(index[0], index[1], z), self.strip(l[0], l[1], z)]
              for z in range(1, M+1)] for l in
             [self.lower_index(x, index, M) for x in
              itertools.product(range(0, int(math.sqrt(M))),
                                range(0, int(math.sqrt(M))))
              if self.lower_index(x, index, M) != [index[0], index[1]]]]
        ))

    def get_rules(self, M):
        """
        get_rules returns all the suduko rules of a sudo of size M.
        """
        return list(itertools.chain.from_iterable(
            list(itertools.chain.from_iterable(
                [[self.get_boxrules(x, M), self.get_unaryrules(x, M),
                  self.at_least_one_rules(x, M), self.get_columnrules(x, M),
                  self.get_rowrules(x, M)] for x in itertools.product(range(1, M+1),
                                                                      range(1, M+1))]
            ))
        ))

    def solve(self, sudoku):
        return [x for x in pycosat.solve(self.get_rules(9) + sudoku) if x > 0]




def main():

    solver = SudokuSolver()
    path = "/home/mas/Desktop/sudoko-sat-solver/dataset/"
    path_sol = "/home/mas/Desktop/sudoko-sat-solver/solversolution/"
    path_converted_sol = "/home/mas/Desktop/sudoko-sat-solver/convertedsol/"
    time_file_path = path_sol + "compute_time.txt"
    time_file = open(time_file_path, "w")
    io = SudokuIO
    compute_time = []
    for n in range(5,6):
        for i in range(0,3):
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

            #convery the normal input from data set to a readable form for sat solver:
            solver_input = io.dataset_parse(readfile)

            #solving evey puzzle and estimate its running time and saving the time records:
            start_time = time.time()
            solution = solver.solve(solver_input)
            end_time = time.time()
            time_object = [n,i,end_time - start_time]
            compute_time.append(time_object)
            time_file.write(str(time_object))
            time_file.write(" ")

            #saving our predicted solutions to file
            print("i:",i,"solution:",solution,'\n')
            io.save_solution(writefile, solution)
            io.save_solution_without_index(converted_sol, solution)

    time_file.write('\n')
    time_file.close()
    print(compute_time)









'''    sudoku = [[219], [714], [328], [425], [821], [331], [836], [938], [441], 
              [843], [554], [655], [757], [265], [667], [277], [579], [772],
              [383], [486], [198]]'''


if __name__ == "__main__":
    main()

