import numpy as np
import random
import os
n = 9 #number of subgrids
m = 3 #number of main grids
init_sudoku = np.array([[(((x//m)+(m*(x%m))+y)%n)+1 for y in range(0,9)] for x in range(0,9)])


class SudoGenerator(object):

    table = init_sudoku

    def sub_swap_rows(self, row1, row2):
        self.table[[row1, row2],:] = self.table[[row2, row1],:]

    def sub_swap_cols(self, col1, col2):
        self.table[:,[col1, col2]] = self.table[:,[col2, col1]]

    def sub_swap_horiz(self,horiz_group1, horiz_group2):
        i = 3 * horiz_group1
        j = 3 * horiz_group2
        self.sub_swap_rows(i,j)
        self.sub_swap_rows(i+1, j+1)
        self.sub_swap_rows(i+2, j+2)

    def sub_swap_vert(self,vert_group1, vert_group2):
        i = 3 * vert_group1
        j = 3 * vert_group2
        self.sub_swap_cols(i,j)
        self.sub_swap_cols(i+1, j+1)
        self.sub_swap_cols(i+2, j+2)

    def swap_rows_of_group(self):
        row_group_num = random.randint(0,2)
        row1 = random.randint(row_group_num*3,row_group_num*3+2)
        allowed_values = list(range(row_group_num*3, row_group_num*3+3))
        allowed_values.remove(row1)
        row2 = random.choice(allowed_values)
        self.sub_swap_rows(row1,row2)

    def swap_cols_of_group(self):
        col_group_num = random.randint(0,2)
        col1 = random.randint(col_group_num*3, col_group_num*3+2)
        allowed_values = list(range(col_group_num*3, col_group_num*3+3))
        allowed_values.remove(col1)
        col2 = random.choice(allowed_values)
        self.sub_swap_cols(col1,col2)

    def swap_vert_two_groups(self):
        vert_group1 = random.randint(0, 2)
        allowed_values = list(range(0, 3))
        allowed_values.remove(vert_group1)
        vert_group2 = random.choice(allowed_values)
        self.sub_swap_vert(vert_group1,vert_group2)

    def swap_horiz_two_groups(self):
        horiz_group1 = random.randint(0, 2)
        allowed_values = list(range(0, 3))
        allowed_values.remove(horiz_group1)
        horiz_group2 = random.choice(allowed_values)
        self.sub_swap_horiz(horiz_group1,horiz_group2)

    def transpose_sudo(self):
        self.table = np.transpose(self.table)

    def swap_two_values(self):
        val1 = random.randint(1, 9)
        allowed_values = list(range(1, 10))
        allowed_values.remove(val1)
        val2 = random.choice(allowed_values)
        self.table[self.table == val1] = -1
        self.table[self.table == val2] = val1
        self.table[self.table == -1] = val2


    def random_transform(self):
        swap_type = random.randint(1, 6)
        #swap_type = 4
        if swap_type == 1:
            self.swap_rows_of_group()
        elif swap_type == 2:
            self.swap_cols_of_group()
        elif swap_type == 3:
            self.swap_vert_two_groups()
        elif swap_type == 4:
            self.swap_horiz_two_groups()
        elif swap_type == 5:
            self.transpose_sudo()
        elif swap_type == 6:
            self.swap_two_values()
        return 0

    def eliminate(self, n):
        table_copy = self.table.copy()
        given = []
        for i in range(0, n):
            index = [random.randint(0, 8), random.randint(0, 8)]
            while index in given:
                index = [random.randint(0, 8), random.randint(0, 8)]
            given.append(index)
        for i in range(0, 9):
            for j in range(0, 9):
                if not ([i, j] in given):
                    table_copy[i][j] = 0
        # remove some elemnts from table_copy
        return table_copy

    def get_next(self, n, path="", counter=-1, write=False):
        self.random_transform()
        self.random_transform()
        puzzle = self.eliminate(n)
        if write:
            self.write_to_disk(puzzle, path+"puzzle_", counter)
            self.write_to_disk(self.table, path + "solution_", counter)
        return puzzle

    def write_to_disk(self, puzzle, path, counter):
        file = open(path+str(counter)+".txt", "w")
        for i in range(9):
            for j in range(9):
                file.write(str(puzzle[i][j]))
            file.write('\n')
        file.close()


path = "data/"
gen = SudoGenerator()
for n in range(1, 81):

    if not os.path.exists(path+str(n)+"/"):
        os.mkdir(path+str(n))
    for i in range(100):
        gen.get_next(n, path=path+str(n)+"/", counter=i, write=True)
