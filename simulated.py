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
import pandas as pd

class Simulated:
    def __init__(self,cube,tmin=0,tmax=100,cooling_schedule='linear',alpha = None,step_max = 1000,greedy_move=False,function_error = 'absolute'):
        '''
        parameters:
        - intial_state -> give the initial state of the problem space
    
        - tmin -> temperature for lower bound
        - tmax -> temperature for upper bound
        - cooling_schedule -> how we want the cooling (either linear or quadratic)
        - alpha -> hyperparamater for cooling schedule
        - step_max -> limitation step that agent can take
        - greedy_move -> move function with greed search approach (best apporach)
        - function_error -> whether the differences on objective function use squared error or absolute error
        '''

        # Check Parameter
        assert cooling_schedule in ['linear','quadratic'],'cooling schedule must be either linear or quadratic'
        assert function_error in ['squared','absolute'], 'function error must be either squared or absolute'
        
        # Initialization
        self.hist = []
        self.t = tmax # Moved Temperature
        self.tmin = tmin
        self.tmax = tmax
        self.cooling_schedule = cooling_schedule
        self.step_max = step_max

        if function_error == 'squared':
            self.function_error = True
        else:
            self.function_error = False


        self.cube = copy.deepcopy(cube)
    
        self.current_energy = self.cube.objective_function(square_error = self.function_error)

        self.initial_state = copy.deepcopy(self.cube)

        self.current_state = copy.deepcopy(self.cube)
        self.best_state = copy.deepcopy(self.current_state)
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
        
        self.start_time = timeit.default_timer()
        self.stuck_ctr = 0
        self.step_stuck = []
        while self.t >= self.tmin and self.step < self.step_max and self.t > 0:

            
            choosen_neighbor = self.move(greedy_move=greedy_move)
            e_n = choosen_neighbor.objective_function(square_error = self.function_error)

            de = e_n - self.current_energy
            if de < 0:
                probability = 1
            else:
                probability = self.safe_exp(-de/self.t)

            print(50*"- -")
            print(f"Step:{self.step},Neighbor's Energy: {e_n}, Best Energy: {self.best_energy}, de: {de}, Temperature: {self.t}, Probability: {probability}\n")
            print(50*"- -")

            if de < 0:
                self.current_energy = e_n
                self.current_state = copy.deepcopy(choosen_neighbor)
                self.accept += 1
            else:
                rand_val = random.random()
                if rand_val < probability:
                
                    self.stuck_ctr += 1
                    self.step_stuck.append(self.step)
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
                    probability,
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
        print(f'    initial energy: {self.initial_state.objective_function(square_error = self.function_error):0.3f}\n')
        print(f'    final energy: {self.best_energy:0.3f}')
        print(f'    energy differences: {(self.initial_state.objective_function(square_error = self.function_error) - self.best_energy):0.3f}\n')

        print(f'    frequency stuck: {self.stuck_ctr}')
        print(f'    ratio stuck: {self.stuck_ctr/self.step}\n')
        
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
    def move(self,greedy_move = False):
        n = self.cube.max_len()
        if greedy_move == True:
            '''
            This is move when you want a greedy move inside the algorithm
            '''
            best_neighbor = copy.deepcopy(self.current_state)
            candidate = copy.deepcopy(self.current_state)
            best_energy = self.best_energy
            for _ in range(10):
                p1 = (np.random.randint(0, n), 
                        np.random.randint(0, n), 
                        np.random.randint(0, n))
                p2 = p1
                while p2 == p1:
                    p2 = (np.random.randint(0, n), 
                            np.random.randint(0, n), 
                            np.random.randint(0, n))
                candidate.array[p1], candidate.array[p2] = candidate.array[p2], candidate.array[p1]
                temp_energy = candidate.objective_function(square_error = self.function_error)

                if temp_energy < best_energy:
                    best_neighbor = copy.deepcopy(candidate)
                    best_energy = temp_energy
                
                candidate.array[p2], candidate.array[p1] = candidate.array[p1], candidate.array[p2]
            return best_neighbor
        else:
            neighbor = copy.deepcopy(self.current_state)
            p1 = (np.random.randint(0, n), 
                        np.random.randint(0, n), 
                        np.random.randint(0, n))
            p2 = p1
            while p2 == p1:
                p2 = (np.random.randint(0, n), 
                        np.random.randint(0, n), 
                        np.random.randint(0, n))
            neighbor.array[p1], neighbor.array[p2] = neighbor.array[p2], neighbor.array[p1]
            return neighbor
    
    # Safe Exponential 
    def safe_exp(self,x):
        '''
        to avoid Math Range error
        '''    
        try:
            return max(-700,min(700,np.exp(x)))
        except:
            return 0

    # Hist Plot

    def hist_plot(self, title=None, Curr_energy=True, Best_energy=True,freq_stuck = False):

        hist = np.array(self.hist)
        

        _, ax = plt.subplots(1, 1, figsize=(25, 5))


        if Curr_energy:
            ax.plot(hist[:, 0], hist[:, 2], linestyle='-', label='Current Energy', color='grey')
        if Best_energy:
            ax.plot(hist[:, 0], hist[:, 3], linestyle='-', label='Best Energy', color='black')
        
        if freq_stuck:
            stuck_x = hist[self.step_stuck, 0]  
            stuck_y = hist[self.step_stuck, 2] 
            ax.scatter(stuck_x, stuck_y, color='red', label='Stuck Points', zorder=5, marker='.')
        

        ax.set_xlabel('Step')
        ax.set_ylabel('Energy')
        ax.set_title(title)
        ax.legend()

        plt.show()

    def prob_plot(self,title=None):
        hist = np.array(self.hist)
        _, ax = plt.subplots(1, 1, figsize=(15, 10))

        ax.plot(hist[:,0],hist[:,4],linestyle='-',marker='',label='Probability',color='green')
        # ax.plot(hist[:,0],hist[:,4],marker='.',linestyle='',label='Probability',color='green')
        ax.set_xlabel('Step')
        ax.set_ylabel('Probability')
        ax.set_title(title)
        ax.legend()
        plt.show