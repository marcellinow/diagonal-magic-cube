import numpy as np
from tensor import *
import copy

class Sideway:
    def __init__(self,cube,limit = 100):

        self.cube = cube

        self.current_state = copy.deepcopy(self.cube)
        self.best_state = copy.deepcopy(self.current_state)

        self.current_value = self.cube.objective_function()
        self.best_value = self.current_value

        self.proposed_neighbor = copy.deepcopy(self.cube)
        self.hist = []

        self.isGoal = False
        self.step = 0

        while self.step < limit:
            
            neighbor = self.bestNeighbors()

            if neighbor.objective_function() < self.best_value:
                self.best_value = neighbor.objective_function()
            self.step += 1
            

    def swap(self):
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

        return self.cubes
    
    def bestNeighbors(self):
        heuristic_cube = copy.deepcopy(self.current_state)
        proposed_neighbors =[]
        n = heuristic_cube.max_len()
        num_neighbors = int((n * (n-1))/2)

        for _ in range(num_neighbors):
            new_cube = copy.deepcopy(heuristic_cube.swap())
            
            if new_cube.objective_function() < heuristic_cube.objective_function():
                proposed_neighbors.append(new_cube)

        best_neighbor = proposed_neighbors[0]
        optimized_value = best_neighbor.objective_function()

        for neighbor in proposed_neighbors[1:]:
            neighbor_value = neighbor.objective_function()
            if neighbor_value < optimized_value:
                best_neighbor = neighbor
        return best_neighbor




