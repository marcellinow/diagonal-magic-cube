import numpy as np
from tensor import *
import copy

class Sideway:
    def __init__(self,cube,limit = 100):

        self.cube = cube

        self.move = 0

        self.current_state = copy.deepcopy(self.cube)
        self.best_state = copy.deepcopy(self.current_state)

        self.current_value = self.cube.objective_function()
        self.best_value = self.current_value

        self.proposed_neighbor = copy.deepcopy(self.cube)
        self.hist = []

        self.isGoal = False

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

        return self.cubes
    
    def calculateNeighbors(self):
        return x

    def bestlNeighbors(self):
        heuristic_cube = copy.deepcopy(self.cube)
        proposed_neighbors =[]
        for _ in range(heuristic_cube.h):
            for _ in range(heuristic_cube.r):
                for _ in range(heuristic_cube.c):
                    new_cube = copy.deepcopy(heuristic_cube.move())

                    if new_cube.objective_function() < heuristic_cube.objective_function():
                        proposed_neighbors.append(new_cube)
        
        for i in range(len(proposed_neighbors)):
            optimized_value = proposed_neighbors[i]



