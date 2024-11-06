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
        child1, child2 = self.crossover(parent1, parent2)

        self.fitness = []
        self.best_cube = None
        self.best_fitness = 0

    def sort_population_by_fitness(self):
        self.population.sort(key=lambda tensor: tensor.objective_function(), reverse=False)

    def crossover(self, parent1, parent2):
        child1 = Tensor(parent1.r, parent1.c, parent1.h)
        child2 = Tensor(parent2.r, parent2.c, parent2.h)
        child1.array = np.copy(parent1.array)
        child2.array = np.copy(parent2.array)

        row = random.randint(0, parent1.r - 1)
        col = random.randint(0, parent1.c - 1)
        height = random.randint(0, parent1.h - 1)

        child1.array[row, col, height], child2.array[row, col, height] = parent2.array[row, col, height], parent1.array[row, col, height]

        return child1, child2
        