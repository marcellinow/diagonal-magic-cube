import numpy as np
from tensor import *
import copy

class Sideway:
    def __init__(self,cube,max_sideway_move = 100):

        self.cube = cube

        self.current_state = copy.deepcopy(self.cube)
        self.best_state = copy.deepcopy(self.current_state)

        self.current_value = self.cube.objective_function()
        self.best_value = self.current_value

        self.hist = []

        self.step = 0
        self.sideway_ctr = 0

        isTerminate = False
        while isTerminate == False:
            if self.best_value != 0:
                neighbors= self.bestNeighbors()
                if (neighbors.objective_function() == 0):
                    self.best_state = neighbors
                    self.best_value = neighbors.objective_function()
                    break

                if neighbors.objective_function() == self.current_value:
                    self.sideway_ctr += 1
                    self.sideway_step = 0
                    while (self.sideway_step <= max_sideway_move):
                        choosen_neighbor = self.move()
                        if choosen_neighbor.objective_function() < self.current_value:
                            self.best_state = choosen_neighbor
                            self.current_value = choosen_neighbor.objective_function()
                            break
                        self.sideway_step += 1
                elif neighbors.objective_function() < self.current_value:
                    self.best_value = neighbors.objective_function()
                    self.best_state = neighbors
                else:
                    isTerminate = True
            
            self.hist.append([
                self.step,
                self.sideway_ctr,
                
            ])
            
    def move(self):
        shape = self.cube.shape
        p0 = (np.random.randint(0,shape[0]),
              np.random.randint(0,shape[1]),
              np.random.randint(0,shape[2]))
        p1 = p0
        while p1  == p0:
            p1 = (np.random.randint(0,shape[0]),
              np.random.randint(0,shape[1]),
              np.random.randint(0,shape[2]))
        self.cube.array[p0], self.cube.array[p1] = self.cube.array[p1], self.cube.array[p0]

        return self.cube
    
    def bestNeighbors(self):
        heuristic_cube = copy.deepcopy(self.current_state)
        proposed_neighbors =[]
        n = heuristic_cube.max_len()
        num_neighbors = int((n * (n-1))/2)

        for _ in range(num_neighbors):
            new_cube = copy.deepcopy(self.move())

            if new_cube.objective_function() < heuristic_cube.objective_function():
                proposed_neighbors.append(new_cube)

        best_neighbor = proposed_neighbors[0]
        optimized_value = best_neighbor.objective_function()

        for neighbor in proposed_neighbors[1:]:
            neighbor_value = neighbor.objective_function()
            if neighbor_value < optimized_value:
                best_neighbor = neighbor
        return best_neighbor