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
import matplotlib.pyplot as plt
import copy
import timeit

class Simulated:
    def __init__(self,cube,tmin=0,tmax=100,cooling_schedule='linear',alpha = None,step_max = 1000):
        '''
        parameters:
        - intial_state -> give the initial state of the problem space
    
        - tmin -> temperature for lower bound
        - tmax -> temperature for upper bound
        - cooling_schedule -> how we want the cooling (either linear or quadratic)
        - alpha -> hyperparamater for cooling schedule
        - step_max -> limitation step that agent can take
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

        self.initial_state = copy.deepcopy(self.cube)

        self.current_state = copy.deepcopy(self.cube).current_state
        self.best_state = copy.deepcopy(self.current_state)
        self.current_energy = self.obj_func
        self.best_energy = self.current_energy

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
        self.start_time = timeit.default_timer()
        stuck_ctr = 0
        while self.t >= self.tmin and self.step < self.step_max and self.t > 0:

            choosen_neighbor = self.move()
            e_n = choosen_neighbor.objective_function()

            de = e_n - self.current_energy

            random_num = random.random()
            accept_prob = -de/self.t
            probability = self.safe_exp(accept_prob)
            print(100*"=")
            print(f"Step:{self.step}, Energy: {e_n}, Best Energy: {self.best_energy},Temperature: {self.t}, Probability: {probability}\n")
            print(100*"=")
            if random_num < probability:
                self.current_energy = e_n
                self.current_state = copy.deepcopy(choosen_neighbor)
                self.accept += 1

            if e_n < self.best_energy:
                self.best_energy = e_n
                self.best_state = copy.deepcopy(choosen_neighbor)

            self.hist.append(
                [
                    self.step,
                    self.t,
                    e_n,
                    self.best_energy,
                    probability
                ]
            )

            self.t = self.update_t(self.step)
            self.step +=1
        self.stop_time = timeit.default_timer()
        self.acceptance_rate = self.accept / self.step
    def final_state(self):
        return Tensor(5,5,5,self.best_state.array)
    def results(self):
        print('+------------------------ RESULTS -------------------------+\n')
        print(f'    cooling sched.: {self.cooling_schedule}')
        print(f'    initial temp: {self.tmax}')
        print(f'    final temp: {self.t}')
        print(f'    final step: {self.step}\n')
        print(f'    initial energy: {self.initial_state.objective_function():0.3f}')
        print(f'    final energy: {self.best_energy:0.3f}\n')
        print(f'    energy differences: {(self.initial_state.objective_function() - self.best_energy):0.3f}\n')
        print(f'    runtime: {(self.stop_time - self.start_time):0.3f} seconds\n')
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
        p1 = (np.random.randint(0, shape[0]), 
                np.random.randint(0, shape[1]), 
                np.random.randint(0, shape[2]))
        p2 = p1
        while p2 == p1:
            p2 = (np.random.randint(0, shape[0]), 
                    np.random.randint(0, shape[1]), 
                    np.random.randint(0, shape[2]))
        
        self.cube.array[p1], self.cube.array[p2] = self.cube.array[p2], self.cube.array[p1]
        return self.cube
    
    # Safe Exponential to avoid Math Range error
    def safe_exp(self,x):
        try:
            return exp(x)
        except:
            return 0

    # Hist Plot
    def hist_plot(self, title=None, Curr_energy=True, Best_energy=True):
        hist = np.array(self.hist)
        _, ax = plt.subplots(1, 1, figsize=(20, 5))

        if Curr_energy == True:
            ax.plot(hist[:, 0], hist[:, 2],linestyle='-', label='Current Energy',color='grey')
        if Best_energy == True:
            ax.plot(hist[:, 0], hist[:, 3],linestyle='-', label='Best Energy',color='black')

        ax.set_xlabel('Step')
        ax.set_ylabel('Energy')
        ax.set_title(title)
        ax.legend()
        plt.show()

    def prob_plot(self,title=None):
        hist = np.array(self.hist)
        _, ax = plt.subplots(1, 1, figsize=(50, 10))

        ax.plot(hist[:,0],hist[:,4],linestyle='-',label='Probability',color='green')
        ax.set_xlabel('Step')
        ax.set_ylabel('Probability')
        ax.set_title(title)
        ax.legend()
        plt.show