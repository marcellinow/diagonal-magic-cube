# Import Relevant Libraries
import random
import numpy as np
from math import exp
from tensor import *

class Random_restart:
    def __init__(self,cube,bounds = [],damping = 1):
        '''
        parameters:
        - intial_state -> give the initial state of the problem space
        '''

        # Check Parameter
        
        # Initialization
        self.hist = []
        self.cube = cube
        self.obj_func = self.cube.objective_function()
        self.damping = damping
        self.bounds = bounds[:]
        self.done = False
        self.current_state = cube.current_state
        self.best_state = self.current_state
        self.current_value = self.obj_func
        self.best_value = self.current_value

        print(f"Initial Value: {self.current_value}\n")

        # optimization

        self.step = 1
        print(f"Initial State: {self.current_state}\n")

        while self.done == False:
            
            choosen_neighbor = self.move()
            print(f"choosen_neighbor = {choosen_neighbor.array}\n")
            # print(f"best_value = {self.best_value}\n")
            value = choosen_neighbor.objective_function()
            if value <= self.current_value:
                self.current_value = value
                self.current_state = choosen_neighbor
                self.done = True


            if value <= self.best_value:
                self.best_value = value
                self.best_state = choosen_neighbor

            self.hist.append(
                [
                    self.step,
                    self.current_value,
                    self.best_value
                ]
            )

            self.step +=1
            print(f"value: {self.current_value}\n")

        
        
    def final_state(self):
        return Tensor(5,5,5,self.best_state).print_tensor()
    def results(self):
        print('+------------------------ RESULTS -------------------------+\n')
        # print(f'      opt.mode: {self.obj_func}')
        # if self.damping != 1: print(f'       damping: {self.damping}\n')
        # else: print('\n')
        print(f'    final step: {self.step}\n')

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
        ax.plot(hist[:, 0], hist[:, 2], label='Objective Function')
        ax.set_xlabel('Step')
        ax.set_ylabel('Value')
        ax.legend()
        plt.show()