def dataset_parse(filename):
    x = 1
    temp_sudo = []
    with open(filename, "r") as fileobj:
        for line in fileobj:
            y = 1
            for ch in range(len(line) - 1):
                if line[ch] != '0':
                    temp_sudo.append(str(x) + str(y) + line[ch])#['223', '337', '342', '393', '584', '659', '683', '734', '773', '788']
                y += 1
            x += 1

    ready_to_solve = [[int(ch)] for ch in temp_sudo]#[[223], [337], [342], [393], [584], [659], [683], [734], [773], [788]]
    return ready_to_solve

def save_solution(filename, solution):
    file = open(filename, "w")
    for obj in solution:
        file.write(str(obj))
        file.write(" ")
    file.write('\n')
    file.close()


def save_solution_without_index(filename, solution):
    file = open(filename, "w")
    prev_index = 1
    for obj in solution:
        list_of_ints = [int(i) for i in str(obj)]
        new_index = list_of_ints[0]
        if new_index == prev_index:
            file.write(str(list_of_ints[2]))
        else:
            file.write('\n')
            file.write(str(list_of_ints[2]))
        prev_index = list_of_ints[0]
    file.write('\n')
    file.close()
