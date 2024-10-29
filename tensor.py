'''
Module to create the cubic

'''

import random
import numpy as np

class Tensor:

    def __init__(self,r,c,h):
        '''
        Where
        r = row
        c = column
        h = height
        '''
        # Instantiate
        self.r = r
        self.c = c
        self.h = h
        
        # Auto make tensor  r x c x h   with rank h
        self.array = []

        # Inialize the tensor with value 0

        for i in range(h):
            h_array = []
            for j in range(r):
                j_array = [0] * c
                h_array.append(j_array)
            self.array.append(h_array)


    def print_tensor(self):
        level = self.h
        for height in self.array:
            print(f"Level: {len(height)-level+1}\n")
            level = level - 1
            for row in height:
                print(row)
            print()

    def is_in_tensor(self, v):
        '''
        Function to check whether the value in the tensor or not
        
        '''
        for height in self.array:
            for row in height:
                if v in row:
                    return True
        return False
    
    def max_len(self):
        return max(self.r,self.c,self.h)

    def initial_state(self):
        '''
        Function to make initial state the tensor

        Requirements:
        Values in range 1 to  n^3 
        where:
        n^3 is max(r,c,h)

        and there are no same value in it

        '''
        n = self.max_len()
        n = n ** 3
        
        for height in self.array:
            for row in height:
                for col in range(len(row)):
                    v = random.randint(1, n)
                    while self.is_in_tensor(v):
                        v = random.randint(1, n)
                    row[col] = v
        return self


    '''
    Magic Cube Functions
    '''

    def magic_constant(self):
        n = self.max_len()
        return ((n * ( (n ** 3)+1))/2)
    
    def straight_line(self):
        n = self.max_len()
        return  3 * n ** 2 + 6* n + 4
    
    def objective_function(self):
        Z = 0
        n = self.max_len()
        MC = self.magic_constant()

        # Row
        # print("--ROW--")
        for level in range(n):
            # print(f"Level: {level+1}\n")
            for row in range(n):
                # print(f"Row: {row+1}\n")
                row_sum = np.sum(self.array[level][row][:])
                # print(f"Row Sum: {row_sum}\n")
                Z += (row_sum - MC) ** 2
                # print(f"Z: {Z}\n")
        # print("\n")
        # print("--COLUMN--")
        # Column
        for level in range(n):
            # print(f"Level: {level+1}\n")
            for col in range(n):
                # print(f"Column: {col+1}\n")
                col_sum = np.sum(self.array[level][:][col])
                # print(f"Col Sum: {col_sum}\n")
                Z += (col_sum - MC) ** 2
                # print(f"Z: {Z}\n")
        # Main Diagonal
        for level in range(n):
            # print(f"Level: {level+1}\n")
            for k in range(n):
                diag_sum_right = np.sum(self.array[k][k])
                # print(f"diag_sum_right: {diag_sum_right}\n")
                diag_sum_left = np.sum(self.array[k][n-1])
                # print(f"diag_sum_left: {diag_sum_left}\n")
                Z += ((diag_sum_right + diag_sum_left) - MC) ** 2
                # print(f"diag_sum: {diag_sum_left + diag_sum_right}\n")

        return Z