'''
Genetic Algorithm Module 
'''

'''
Applied genetic algorithm in diagonal magic cube problem
'''

# Import Relevant Libraries
import random
import numpy as np
from math import exp
from tensor import *

class GeneticAlgo:
    def __init__(self, cube, goal_cube, population_size, generation_rate, mutation_rate):
        self.cube = cube
        goal_cube = goal_cube
        self.population_size = population_size
        self.generation_rate = generation_rate
        self.mutation_rate = mutation_rate
        
        # Population
        self.population = []
        self.population.append(cube)
        while len(self.population) < self.population_size:
            new_cube = cube.initial_state(self.cube)
            if not cube.same_tensor(new_cube):
                self.population.append(new_cube)
        self.sort_population_by_fitness(self)

        # Selection
        self.population = self.population[:2]
        parent1 = self.population[0]
        parent2 = self.population[1]

        # Crossover
        child = self.crossover(parent1, parent2)

        
        self.fitness = []
        self.best_cube = None
        self.best_fitness = 0

    def sort_population_by_fitness(self):
        self.population.sort(key=lambda tensor: tensor.objective_function(), reverse=True)

    def crossover(self, parent1, parent2):
        child = Tensor(parent1.r, parent1.c, parent1.h)
        for i in range(parent1.r):
            for j in range(parent1.c):
                for k in range(parent1.h):
                    if random.random() < 0.5:
                        child.array[i][j][k] = parent1.array[i][j][k]
                    else:
                        child.array[i][j][k] = parent2.array[i][j][k]
        return child
        