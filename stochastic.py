# Import Relevant Libraries
import random
import numpy as np
from tensor import *

import copy

class Stochastic:
    def __init__(self, cube, max_iterations=100):
        '''
        parameters:
        - cube -> initial state of the problem space
        - max_iterations -> maximum number of iterations to run the algorithm
        '''

        # Initialization
        self.hist = []
        self.cube = copy.deepcopy(cube)
        self.obj_func = self.cube.objective_function()
        self.done = False
        self.neighbor_checked = 0
        self.current_state = copy.deepcopy(self.cube)
        self.best_state = copy.deepcopy(self.current_state)
        self.current_value = self.obj_func
        self.best_value = self.current_value
        self.best_step = 0
        self.max_iterations = max_iterations

        print(f"Initial Value: {self.current_value}\n")

        # Optimization
        self.step = 1
        while self.step <= self.max_iterations:
            neighbor = self.random_successor()
            neighbor_value = neighbor.objective_function()

            if neighbor_value < self.best_value:
                print(f"Step {self.step}: Chosen Neighbor Value: {neighbor_value}; Best Value: {self.best_value}")
                self.best_value = neighbor_value
                self.current_state = neighbor
                self.step += 1
                self.hist.append(
                    [
                        self.step,
                        neighbor_value,
                        self.best_value
                    ]
                )
                self.best_step = self.step
            else:
                self.step += 1

    def random_successor(self):
        successor_cube = copy.deepcopy(self.current_state)
        successor_cube = successor_cube.randomize_value()
        return successor_cube

    def final_state(self):
        return Tensor(5, 5, 5, self.best_state)

    def results(self):
        print('+------------------------ RESULTS - -------------------------+\n')
        print(f'    Best step: {self.best_step}\n')
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