'''
Module to create the cubic

'''

import random

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
    

    # Specs Function

    def check_column_sum(self):
        '''
        Function to check if the sum of each column of the matrix is the same
        '''
        sum_columns = []
        
        for height in self.array:
            for col in range(self.c):
                sum_columns.append(sum(height[row][col] for row in range(self.r)))

        if len(set(sum_columns)) == 1:
            return True
        else:
            return False
        

    def check_row_sum(self):
        '''
        Function to check if the sum of each row of the matrix is the same
        '''
        sum_rows = []

        for height in self.array:
            for row in range(self.r):
                sum_rows.append(sum(height[row][col] for col in range(self.c)))

        if len(set(sum_rows)) == 1:
            return True
        else:
            return False
    
    def check_diagonal_sum(self):
        '''
        Function to check if the sum of main diagonal of the matrix is the same
        '''

        sum_diagonal = []

        for height in self.array:
            first_diag_sum = 0
            second_diag_sum = 0
            for i in range(self.r):
                first_diag_sum += height[i][i]
                second_diag_sum += height[i][self.c - i - 1]
            sum_diagonal.append(first_diag_sum)
            sum_diagonal.append(second_diag_sum)

        if len(set(sum_diagonal)) == 1:
            return True
        else:
            return False

    def is_magic_cube():
        '''
        '''