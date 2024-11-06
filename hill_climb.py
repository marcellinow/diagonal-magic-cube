# Import Relevant Libraries
import random
import numpy as np
from math import exp
from tensor import *

import copy
class Hill_climb:
    def __init__(self,cube):
        '''
        parameters:
        - intial_state -> give the initial state of the problem space
        '''

        # Check Parameter
        
        # Initialization
        self.hist = []
        self.cube = cube
        self.obj_func = self.cube.objective_function()
        self.done = False
        self.neighbor_checked = 0
        self.current_state = copy.deepcopy(self.cube)
        self.best_neighbor = self.current_state
        self.best_state = self.current_state
        self.current_value = self.obj_func
        self.best_value = self.current_value
        self.best_neighbor_value = float('inf')


        print(f"Initial Value: {self.current_value}\n")

        # optimization

        self.step = 1
        # print(f"Initial State: {self.current_state}\n")
        
        while True:
            print("START!")
            self.best_neighbor,self.best_neighbor_value = self.best_successor()
            print("WLELWELWE")
            
            print("Ifelse Statement")
            if self.best_neighbor_value < self.best_value:
                print(f"Step {self.step}: Choosen Neighbor Value: {self.best_neighbor_value}; Best Value: {self.best_value}")
                self.best_value = self.best_neighbor_value
                self.current_state = self.best_neighbor
                self.step +=1
                self.hist.append(
                [
                    self.step,
                    self.best_neighbor_value,
                    self.best_value
                ]
            )
            
            else:
                break
            #Kodingan Nathan
            # if self.best_neighbor_value > self.best_value:
            #     while self.neighbor_checked <= 10:
            #         choosen_neighbor = self.move()
            #         # print(f"choosen_neighbor = {choosen_neighbor.array}\n")
            #         # print(f"best_value = {self.best_value}\n")
            #         value = choosen_neighbor.objective_function()
            #         if value < self.current_value:
            #             self.current_value = value
            #             self.current_state = choosen_neighbor

            #         if value < self.best_neighbor_value:
            #             self.best_neighbor_value = value
            #             self.best_neighbor = choosen_neighbor
            #         self.neighbor_checked += 1

            #         print (f"neighbor checked= {self.neighbor_checked}\n")
            #         print(f"current_value = {self.current_value}\n")
                

            # else :
            #     self.best_value = self.best_neighbor_value
            #     self.best_state = self.best_neighbor
            #     self.done = True
            
    def best_successor(self):
        # print("Finding Best Successor...\n")
        # print("Current Cube:\n", current_cube)

        
        neighbors = []
        
        n = self.cube.max_len()
        num_neighbors = int((n * (n - 1)) / 2)  

        
        for _ in range(num_neighbors):
            successor_cube = copy.deepcopy(self.current_state)
            successor_cube = successor_cube.randomize_value()
            neighbors.append(successor_cube)
        
        best_neighbor = neighbors[0]
        best_neighbor_value = best_neighbor.objective_function()

        
        for neighbor in neighbors[1:]:
            neighbor_value = neighbor.objective_function()
            if neighbor_value < best_neighbor_value:
                best_neighbor = neighbor
                best_neighbor_value = neighbor_value

        
        return best_neighbor, best_neighbor_value



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