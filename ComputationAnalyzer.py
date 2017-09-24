import SudokuIO as io
import time
import os
import SudokuSolver as ss
import matplotlib.pyplot as plt

def main():

    max_given_num = 80
    samples_num = 3
    path = "/home/mas/Desktop/sudoko-sat-solver/dataset/"
    path_sol = "/home/mas/Desktop/sudoko-sat-solver/solversolution/"
    path_converted_sol = "/home/mas/Desktop/sudoko-sat-solver/convertedsol/"
    time_file_path = path_sol + "compute_time.txt"


    solver = ss.SudokuSolver()
    compute_time = []
    mean = [0]*max_given_num

    for n in range(1,max_given_num+1):
        time_file = open(time_file_path, "w")
        for i in range(0,samples_num):
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

            mean[n - 1] = mean[n - 1] + (end_time - start_time)

            #saving our predicted solutions to file
            print("i:",i,"solution:",solution,'\n')
            io.save_solution(writefile, solution)
            io.save_solution_without_index(converted_sol, solution)

        mean[n - 1] = (mean[n - 1])/(samples_num*1.0)

        time_file.write('\n')
        time_file.close()
    print(compute_time)
    print("mean: ",mean)
    plt.figure(1)
    x = [i for i in range(1,max_given_num+1)]
    plt.plot(x,mean)
    plt.show()

if __name__ == "__main__":
    main()
