import SudokuIO as io
import time
import os
import SudokuSolver as ss
import matplotlib.pyplot as plt

def variance_compute(compute_time,mean,max_given_num,samples_num):
    var = [0]*max_given_num
    # compute_time = [[1, 0, 0.18725013732910156], [1, 1, 0.14868760108947754], [1, 2, 0.14481735229492188], [2, 0, 0.194868803024292], [2, 1, 0.14738917350769043], [2, 2, 0.156538724899292], [3, 0, 0.2090892791748047], [3, 1, 0.15350747108459473], [3, 2, 0.14542222023010254]]
    for item, row in enumerate(compute_time): # For example: item = [2, 1, 0.14738917350769043]
        for i in range(1, max_given_num + 1):
            if (row[0] == i):
                var[i-1] = var[i-1] + (row[2] - mean[i - 1])**2
    for i in range(len(var)):
        var[i] = var[i] / (samples_num*1.0)
    return var

def mean_compute(compute_time,max_given_num,samples_num):
    mean = [0]*max_given_num
    # compute_time = [[1, 0, 0.18725013732910156], [1, 1, 0.14868760108947754], [1, 2, 0.14481735229492188], [2, 0, 0.194868803024292], [2, 1, 0.14738917350769043], [2, 2, 0.156538724899292], [3, 0, 0.2090892791748047], [3, 1, 0.15350747108459473], [3, 2, 0.14542222023010254]]
    for item, row in enumerate(compute_time): # For example: item = [2, 1, 0.14738917350769043]
        for i in range(1, max_given_num+1):
            if (row[0] == i):
                print(i,"row",row[0])
                mean[i-1] = mean[i-1] + row[2]
    for i in range(len(mean)):
        mean[i] = mean[i] / (samples_num*1.0)
    return mean

def main():

    max_given_num = 80
    samples_num = 100
    path = "/home/mas/Desktop/sudoko-sat-solver/dataset/"
    path_sol = "/home/mas/Desktop/sudoko-sat-solver/solversolution/"
    path_converted_sol = "/home/mas/Desktop/sudoko-sat-solver/solversolution/convertedsol/"
    time_file_path = path_sol + "compute_time.txt"
    mean_file_path = path_sol + "mean.txt"
    var_file_path = path_sol + "variace.txt"

    solver = ss.SudokuSolver()
    compute_time = []

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

            #saving our predicted solutions to file
            io.save_solution(writefile, solution)
            io.save_solution_without_index(converted_sol, solution)

        time_file.write('\n')
        time_file.close()

    mean = mean_compute(compute_time,max_given_num,samples_num)
    var = variance_compute(compute_time, mean, max_given_num, samples_num)

    io.save_solution(mean_file_path, mean)
    io.save_solution(var_file_path, var)

    print(compute_time)
    print("mean: ",mean)
    print("var: ", mean)

    plt.figure(1)
    x = [i for i in range(1,max_given_num+1)]
    plt.subplot(1, 2, 1)
    plt.plot(x,mean)
    plt.xlabel("number of given")
    plt.ylabel("mean")
    plt.subplot(1, 2, 2)
    plt.plot(x, var)
    plt.xlabel("number of given")
    plt.ylabel("variance")
    plt.savefig(path_sol+"plot_for_mean_var_to_n")
    plt.show()









if __name__ == "__main__":
    main()
