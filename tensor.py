'''
Module to create the cubic

'''

import random
import matplotlib.pyplot as plt
import numpy as np

class Tensor:

    def __init__(self,r,c,h,initial_array = None):
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
        self.shape = (r,c,h)

        
        # Auto make tensor  r x c x h   with rank h
        self.array = []

        # Inialize the tensor with value 0
        if initial_array is not None:
            self.array = np.array(initial_array)
        else:
            for _ in range(h):
                h_array = []
                for _ in range(r):
                    j_array = [0] * c
                    h_array.append(j_array)
                self.array.append(h_array)
            self.array = np.array(self.array)

        # state
        self.current_state = self.array

    def print_tensor(self):
        level = self.h
        for height in self.array:
            print(f"Level: {len(height)-level+1}\n")
            level = level - 1
            for row in height:
                print(row)
            print()

    def plot_cube(self,title="Tensor Cube"):
        fig = plt.figure(figsize=(15,15))
        ax = fig.add_subplot(111,projection="3d")
        ax.set_box_aspect([self.r, self.c, self.h])

        for h in range(self.h):
            for r in range(self.r):
                for c in range(self.c):
                    ax.text(r,c,h,f"{self.array[h][r][c]}",ha="center",va="center",fontsize=14,color="blue")
                    ax.scatter(r,c,h,c="orange",s=500,edgecolors="k",alpha=0.4)
            
        ax.set_xlabel("column-axis")
        ax.set_ylabel("row-axis")
        ax.set_zlabel("level")
        plt.title(title)
        return plt.show()
    
    def plot_per_level(self,title="Tensor Cube"):
         for h in range(self.h):
            fig = plt.figure(figsize=(8, 8))
            ax = fig.add_subplot(111, projection="3d")
            ax.set_box_aspect([self.r, self.c, 1])

            # Plot cells within the current level
            for r in range(self.r):
                for c in range(self.c):
                    ax.text(r, c, 0, f"{self.array[h][r][c]}", ha="center", va="center", fontsize=14, color="blue")
                    ax.scatter(r, c, 0, c="orange", s=500, edgecolors="k", alpha=0.4)

            # Labels and title
            ax.set_xlabel("Column-axis")
            ax.set_ylabel("Row-axis")
            ax.set_zlabel("Level")
            plt.title(f"{title} - Level {h + 1}")
            plt.show()

    def same_tensor(self,tensor):
        '''
        Function to check whether the tensor is same or not
        
        '''
        if self.shape != tensor.shape:
            return False
        
        for heigth in range(self.h):
            for row in range(self.r):
                for col in range(self.c):
                    if self.array[heigth,row,col] != tensor.array[heigth,row,col]:
                        return False
        return True
                            
    
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
    
    def randomize_value(self):
        n = self.max_len() ** 3
        shape = self.array.shape
        num_swaps = n // 2
        for _ in range(num_swaps):
            first = (np.random.randint(0, shape[0]), 
                    np.random.randint(0, shape[1]), 
                    np.random.randint(0, shape[2]))
            second = first
            while second == first:
                second = (np.random.randint(0, shape[0]), 
                        np.random.randint(0, shape[1]), 
                        np.random.randint(0, shape[2])) 
            self.array[first], self.array[second] = self.array[second], self.array[first]
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

        # Row, Column, and Level
        for i in range(n):
            for j in range(n):
                row_sum = np.sum(self.array[i,j,:])
                Z += (row_sum - MC) ** 2
                col_sum = np.sum(self.array[i,:,j])
                Z += (col_sum - MC) ** 2 
                level_sum = np.sum(self.array[:,i,j])
                Z += (level_sum - MC) ** 2

                # print(f"Row sum at ({i},{j}): {row_sum}, Column sum at ({i},{j}): {col_sum}, Level sum at ({i},{j}): {level_sum}")

        # Main Diagonal
        for k in range(n):
            diag_sum_first = np.sum(self.array[k,k,k])
            diag_sum_second = np.sum(self.array[k,k,n-1-k])
            diag_sum_third = np.sum(self.array[k,n-1-k,k])
            diag_sum_fourth = np.sum(self.array[n-1-k,k,k])
            Z += ((diag_sum_first + diag_sum_second+diag_sum_third+diag_sum_fourth) - MC) ** 2
            # print(f"diag_sum_first: {diag_sum_first}, diag_sum_second: {diag_sum_second}, diag_sum_third: {diag_sum_third}, diag_sum_fourth: {diag_sum_fourth}\n")
            # print(f"Level {k+1}:")
            # print(f"(k,k,k): {self.array[k,k,k]} ")
            # print(f"  diag_sum_first (k, k, k): {diag_sum_first}")
            # print(f"(k,k,n-1-k): {self.array[k,k,n-1-k]}\n")
            # print(f"  diag_sum_second (k, k, n-1-k): {diag_sum_second}")
            # print(f"(k,n-1-k,k): {self.array[k,n-1-k,k]}\n")
            # print(f"  diag_sum_third (k, n-1-k, k): {diag_sum_third}")
            # print(f"(n-1-k,k,k): {self.array[n-1-k,k,k]}\n")
            # print(f"  diag_sum_fourth (n-1-k, k, k): {diag_sum_fourth}")
            # print(f"  Total diagonal sum at level {k+1}: {diag_sum_first + diag_sum_second + diag_sum_third + diag_sum_fourth}")
            # print(f"  Squared difference from magic constant: {((diag_sum_first + diag_sum_second + diag_sum_third + diag_sum_fourth) - MC) ** 2}")
            print("\n")
        return Z