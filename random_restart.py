# Import Relevant Libraries
import random
import numpy as np
from math import exp
from tensor import *
from hill_climb import Hill_climb as find_local_optimum


import copy
class Random_restart:
    def __init__(self,cube, max_restart=100):
        '''
        parameters:
        - intial_state -> give the initial state of the problem space
        '''

        # Check Parameter

        
        
        # Initialization
        self.hist = []
        self.cube = cube
        self.max_restart = max_restart
        self.obj_func = self.cube.objective_function()
        self.current_state = copy.deepcopy(self.cube)
        self.current_value = self.obj_func
        self.best_state = self.current_state
        self.best_value = self.current_value
        self.iteration = 0
        self.best_iteration = 0
        
        print(f"Initial Value: {self.current_value}\n")

        for i in range(self.max_restart):
            self.local_optimum = find_local_optimum(self.current_state)
            self.local_optimum_value = self.local_optimum.best_value

            if self.local_optimum_value < self.best_value:
                self.best_state = self.local_optimum
                self.best_value = self.local_optimum_value
                
                self.best_iteration = i
            
            self.hist.append(
                [
                    i,
                    self.local_optimum_value,
                    self.best_value
                ]
                )
            
            self.iteration += 1
        print(f"Best Value: {self.best_value}\n")



    def final_state(self):
        return Tensor(5,5,5,self.best_state).print_tensor()
    def results(self):
        print('+------------------------ RESULTS -------------------------+\n')
        # print(f'      opt.mode: {self.obj_func}')
        # if self.damping != 1: print(f'       damping: {self.damping}\n')
        # else: print('\n')
        print(f'    Best iteration: {self.best_iteration}\n')

        print(f'  final Value: {self.best_value:0.6f}\n')
        print('+-------------------------- END ---------------------------+')



    # Move Function
    def move(self):
        shape = self.cube.shape
        
        first = (np.random.randint(0, shape[0]), 
                np.random.randint(0, shape[1]), 
                np.random.randint(0, shape[2]))
        second = first
        while second == first:
            second = (np.random.randint(0, shape[0]), 
                    np.random.randint(0, shape[1]), 
                    np.random.randint(0, shape[2]))
        
        self.cube.array[first], self.cube.array[second] = self.cube.array[second], self.cube.array[first]
        
        return self.cube
        

    # Hist Plot
    
    def hist_plot(self):
        import matplotlib.pyplot as plt
        hist = np.array(self.hist)
        _, ax = plt.subplots(1, 1, figsize=(10, 5))
        ax.plot(hist[:, 0], hist[:, 1], label='Local Optimum Value')
        ax.set_xlabel('Iteration')
        ax.set_ylabel('Value')
        ax.legend()
        plt.show()