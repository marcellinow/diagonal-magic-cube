'''
Simulated Annealing Module 
'''

'''
Applied simulated annealing algorithm in diagonal magic cube problem
reference:
https://nathanrooy.github.io/posts/2020-05-14/simulated-annealing-with-python/
'''

# Import Relevant Libraries
import random
import numpy as np
from math import exp
from tensor import *

class Simulated:
    def __init__(self,cube,tmin=0,tmax=100,cooling_schedule='linear',alpha = None,step_max = 1000,bounds = [],damping = 1):
        '''
        parameters:
        - intial_state -> give the initial state of the problem space
    
        - tmin -> temperature for lower bound
        - tmax -> temperature for upper bound
        - cooling_schedule -> how we want the cooling (either linear or quadratic)
        - alpha -> hyperparamater for cooling schedule
        - step_max -> limitation step that agent can take
        - bounds -> lower and upper bound for variable in objective function
        - damping -> magnitude how much change agent want
        
        '''

        # Check Parameter
        assert cooling_schedule in ['linear','quadratic'],'cooling schedule must be either linear or quadratic'
        
        # Initialization
        self.hist = []
        self.t = tmax # Moved Temperature
        self.tmin = tmin
        self.tmax = tmax
        self.cooling_schedule = cooling_schedule
        self.step_max = step_max

        self.cube = cube
        self.obj_func = self.cube.objective_function()
        self.damping = damping
        self.bounds = bounds[:]

        self.current_state = cube.current_state
        self.best_state = self.current_state
        self.current_energy = self.obj_func
        self.best_energy = self.current_energy

        # Heuristics Atributes
        self.ideal_energy = 1278394.0

        print(f"Initial Energy: {self.current_energy}\n")

        if self.cooling_schedule == 'linear':
            if alpha != None:
                self.update_t = self.cooling_linear_m
                self.cooling_schedule = 'linear multiplicative'
                self.alpha = alpha
            
            if alpha == None:
                self.update_t = self.cooling_linear_a
                self.cooling_schedule = 'linear additive'
        
        elif self.cooling_schedule == 'quadratic':
            if alpha != None:
                self.update_t = self.cooling_quadratic_m
                self.cooling_schedule = 'quadratic multiplicative'
                self.alpha = alpha

            if alpha == None:
                self.update_t = self.cooling_quadratic_a
                self.cooling_schedule = 'quadratic additive'

        # optimization

        self.step = 1
        self.accept = 0
        # print(f"Initial State: {self.current_state}\n")

        while self.step <= self.step_max and self.t >= self.tmin:
        # while self.t >= self.tmin:
            
            choosen_neighbor = self.move()
        
            e_n = choosen_neighbor.objective_function()
    
            de = e_n - self.current_energy
    
            if de < 0:
                accept_prob = 1
            elif self.t > self.tmin:
                accept_prob = exp(-de / self.t)
            else:
                accept_prob = 0

            # if self.t <= 1e-5 or (-de / self.t) < max_argument: 
            random_num = random.random()
            if de < 0 or (self.t >= self.tmin and random_num < accept_prob):
                print(f"Energies: {e_n} < {self.current_energy}\n")
                print(f"Temperature: {self.t}\n")
                print(f"Random: {random.random()}\n")
                print(f"Probability: {accept_prob}\n")

                self.current_energy = e_n
                self.current_state = choosen_neighbor
                self.accept += 1

            if e_n < self.best_energy:
                self.best_energy = e_n
                self.best_state = choosen_neighbor

            self.hist.append(
                [
                    self.step,
                    self.t,
                    self.current_energy,
                    self.best_energy,
                    accept_prob
                ]
            )

            self.t = self.update_t(self.step)
            self.step +=1
        self.acceptance_rate = self.accept / self.step
    def final_state(self):
        return Tensor(5,5,5,self.best_state).print_tensor()
    def results(self):
        print('+------------------------ RESULTS -------------------------+\n')
        # print(f'      opt.mode: {self.obj_func}')
        print(f'cooling sched.: {self.cooling_schedule}')
        # if self.damping != 1: print(f'       damping: {self.damping}\n')
        # else: print('\n')

        print(f'  initial temp: {self.tmax}')
        print(f'    final temp: {self.t:0.6f}')
        print(f'     max steps: {self.step_max}')
        print(f'    final step: {self.step}\n')

        print(f'  final energy: {self.best_energy:0.6f}\n')
        print('+-------------------------- END ---------------------------+')


    def cooling_linear_a(self,step):
        return self.tmin + (self.tmax - self.tmin) * ((self.step_max - step)/self.step_max)
    
    def cooling_linear_m(self,step):
        return self.tmax - self.alpha * step
    
    def cooling_quadratic_m(self,step):
        return self.tmax / (1 + self.alpha * (step ** 2))
    
    def cooling_quadratic_a(self,step):
        return self.tmin + (self.tmax - self.tmin) * (((self.step_max - step)/self.step_max)**2)

    # Move Function
    def move(self):
        shape = self.cube.shape
        # low_t = 0.1 * self.tmax
        
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
        ax.plot(hist[:, 0], hist[:, 3], label='Objective Function')
        ax.set_xlabel('Step')
        ax.set_ylabel('Energy')
        ax.legend()
        plt.show()