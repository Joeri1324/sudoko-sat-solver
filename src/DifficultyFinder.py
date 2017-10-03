import numpy as np
import matplotlib.pyplot as plt


def parse_statiscis(names, stat_path):
    all_givens = []
    stat_file = open(stat_path, "r")
    num_of_givens = int(stat_file.readline().strip())
    num_of_samples = int(stat_file.readline().strip())
    givens = [i for i in range (50,50+num_of_givens)]
    for g in givens:
        results = {}
        for name in names:
            results[name] = []
        sample = 1
        while (True):   # read and process lines for all samples within a given number
            line = stat_file.readline()
            if line[0]=='\'':
                sample += 1

            if line[0:3] == "c 1":
                line = line[3:]
            else:
                continue
            list_of_floats = line.strip().split()
            for i in range(len(names)):
                results[names[i]].append(float(list_of_floats[i]))
            if sample == num_of_samples:
                break
        all_givens.append(results)
    return all_givens

def calculate_difficulty_measure(all_givens, metrics_of_intersts):
    result = {}
    for metric in metrics_of_intersts:
        one_metric = metric
        result[metric] = []
        all_measures = []
        for given in all_givens:
            all_measures += given[metric]
        all_measures_np = np.array(all_measures)
        min_measure = np.amin(all_measures_np)
        max_measure = np.amax(all_measures_np)
        for given in all_givens:
            given_measure_avg = np.mean(np.array(given[metric]))
            result[metric].append(given_measure_avg)
            #given_measure_score = (given_measure_avg-min_measure)/float(max_measure-min_measure)
            #result[metric].append(given_measure_score)
'''    result['total'] = []
    for i in range(len(result[one_metric])):
        total_score = 0
        for metric in metrics_of_intersts:
            total_score += result[metric][i] * metrics_of_intersts[metric]
        result['total'].append(total_score)'''
    return result


names = ['seconds', 'level', 'variables', 'used', 'original', 'conflicts', 'learned', 'limit', 'agility', 'MB']
stat_path = "/home/mas/Desktop/sudoko-sat-solver/solversolution/statistic.txt"
plot_path = "/home/mas/Desktop/sudoko-sat-solver/solversolution/"
all_givens_stat = parse_statiscis(names, stat_path)
measure_of_interst = {}
measure_of_interst["conflicts"] = 1
#measure_of_interst["level"] = 0.3
#measure_of_interst["agility"] = 0
#measure_of_interst["learned"] = 0
result = calculate_difficulty_measure(all_givens_stat, measure_of_interst)
number_of_xpoints = len(result[list(result.keys())[0]]) + 1
number_of_metrics = len(list(result.keys()))


given_number = [i for i in range(1, number_of_xpoints)]
i = 1
for metric in result:
    print(metric, result[metric])
    plt.figure(i)
    plt.plot(given_number, result[metric])
    plt.xlabel("number of given")
    plt.ylabel(metric)
    plt.savefig(plot_path+str(metric))
    i += 1

plt.show()
plt.close()



