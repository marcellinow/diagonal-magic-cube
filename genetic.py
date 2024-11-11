import random
import numpy as np
import matplotlib.pyplot as plt
from tensor import *

class GeneticAlgoNJ:
    def __init__(self, cube, population_size, generation_rate, mutation_rate, elitism_size):
        self.cube = cube
        self.population_size = population_size
        self.generation_rate = generation_rate
        self.mutation_rate = mutation_rate
        self.elitism_size = elitism_size

        # Initialize population
        self.population = [Tensor(cube.r, cube.c, cube.h).initial_state() for _ in range(population_size)]
        self.best_cube = None
        self.best_fitness = float('inf')
        
        # Store fitness history for plotting
        self.fitness_history = []

    def cube_to_array(self, cube):# !Ubah cube jadi array 1D
        numbers = []
        for h in range(cube.h):
            for r in range(cube.r):
                for c in range(cube.c):
                    numbers.append(int(cube.array[h][r][c]))
        return numbers

    def reconstruct_cube(self, flat_array):# !Ubah array 1D jadi Cube
        r, c, h = 5, 5, 5  # Assuming fixed size for simplicity; adjust as needed.
        if len(flat_array) != r * c * h:
            raise ValueError("The size of the flat array does not match the dimensions of the cube.")
        
        reconstructed_array = []
        idx = 0
        for level in range(h):
            level_array = []
            for row in range(r):
                row_array = []
                for col in range(c):
                    row_array.append(flat_array[idx])
                    idx += 1
                level_array.append(row_array)
            reconstructed_array.append(level_array)

        return Tensor(r, c, h, initial_array=reconstructed_array)

    def fitness(self, cube): #! Cek fitness dari suatu cube
       return cube.objective_function()

    def select_parents(self):
       #! dari populasi dipilih secara random cube sebanyak tournament size, trus diambil 2 dengan fitness terbaik
       tournament_size = 5
       selected = random.sample(self.population, tournament_size)
       selected.sort(key=lambda tensor: self.fitness(tensor))
       return selected[0], selected[1]

    def crossover(self, parent1, parent2):
        #! parrent cube diubah jadi 1D array
        parent1_array = self.cube_to_array(parent1)
        parent2_array = self.cube_to_array(parent2)

        #! tentuin bakal dicrossover dimana secara random
        n = len(parent1_array)
        crossover_point = random.randint(0, n - 1)

        #! ambil semua angka dari awal parent 1 sampe crossoverPoint, digabungin dengan semua angka dari parent 2 yang gak ada di parent 1
        child1_array = parent1_array[:crossover_point] + [num for num in parent2_array if num not in parent1_array[:crossover_point]]
        child2_array = parent2_array[:crossover_point] + [num for num in parent1_array if num not in parent2_array[:crossover_point]]

        #! Ubah balik dari 1D array jadi cube
        child1_cube = self.reconstruct_cube(child1_array)
        child2_cube = self.reconstruct_cube(child2_array)

        return child1_cube, child2_cube

    def evolve(self):
       """Evolves the population over generations to find a solution."""
       
       for generation in range(self.generation_rate):
           new_population = []

           # Preserve elites if applicable
           if self.elitism_size > 0:
               elites = sorted(self.population, key=lambda tensor: self.fitness(tensor))[:self.elitism_size]
               new_population.extend(elites)

           while len(new_population) < self.population_size:
               parent1, parent2 = self.select_parents()
               child1, child2 = self.crossover(parent1, parent2)

               if random.random() < self.mutation_rate:
                   child1 = self.mutate(child1)
               if random.random() < self.mutation_rate:
                   child2 = self.mutate(child2)

               # Avoid duplicates in new population
               if child1 not in new_population:
                   new_population.append(child1)
               if child2 not in new_population:
                   new_population.append(child2)

           # Trim new_population to population_size if it exceeds due to duplicates
           self.population = new_population[:self.population_size]

           # Update best solution found and record fitness value
           for cube in self.population:
               fitness_value = self.fitness(cube)
               if fitness_value < self.best_fitness:
                   self.best_fitness = fitness_value
                   self.best_cube = cube

           # Record fitness value for this generation
           self.fitness_history.append(self.best_fitness)

    def mutate(self, cube):
       """Mutates a cube by swapping two random elements in its representation."""
       
       flat_array = self.cube_to_array(cube)
       
       idx1, idx2 = random.sample(range(len(flat_array)), 2)
       
       flat_array[idx1], flat_array[idx2] = flat_array[idx2], flat_array[idx1]
       
       mutated_cube = self.reconstruct_cube(flat_array)
       
       return mutated_cube

    def get_best_solution(self):
       """Returns the best solution found and its fitness value."""
       return self.best_cube, self.best_fitness

    def hist_plot(self):
       """Plots the history of fitness values over generations."""
       plt.figure(figsize=(10, 5))
       plt.plot(self.fitness_history, label='Best Fitness Over Generations')
       plt.xlabel('Generation')
       plt.ylabel('Fitness Value')
       plt.title('Fitness Evolution Over Generations')
       plt.legend()
       plt.grid()
       plt.show()