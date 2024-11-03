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

class Simulated:

    def __init__(self,initial_state,obj_func,tmin=0,tmax=100,cooling_schedule='linear',alpha = None,step_max = 1000,bounds = [],damping = 1):
        '''
        parameters:
        - intial_state -> give the initial state of the problem space
        - obj_func -> the objective function 
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

        
        self.obj_func = obj_func
        self.damping = damping
        self.bounds = bounds[:]

        self.current_state = initial_state
        self.best_state = self.current_state
        self.current_energy = obj_func(self.current_state)
        self.best_energy = self.current_energy

        self.get_neighbor = self.move

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

        while self.step <= self.step_max and self.t >= self.tmin and self.t >= 0:
            
            choosen_neighbor = self.get_neighbor()

            e_n = self.obj_func(choosen_neighbor)
            de = e_n - self.current_energy

            if random() < exp(-de/self.t):
                self.current_energy = e_n
                self.current_state = choosen_neighbor[:]
                self.accept+= 1

            if e_n < self.best_energy:
                self.best_energy = e_n
                self.best_state = choosen_neighbor[:]

            self.hist.append(
                [
                    self.step,
                    self.t,
                    self.current_energy,
                    self.best_energy
                ]
            )

            self.t = self.update_t(self.step)
            self.step +=1
        self.acceptance_rate = self.accept / self.step
    
    def results(self):
        print('+------------------------ RESULTS -------------------------+\n')
        print(f'      opt.mode: {self.obj_func.__name__}')
        print(f'cooling sched.: {self.cooling_schedule}')
        if self.damping != 1: print(f'       damping: {self.damping}\n')
        else: print('\n')

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
    # def cooling_linear_m(self, step):
    #     return self.t_max /  (1 + self.alpha * step)
    
    def cooling_quadratic_a(self,step):
        return self.tmax / (1 + self.alpha * (step ** 2))
    
    def cooling_quadratic_m(self,step):
        return self.tmin + (self.tmax - self.tmin) * (((self.step_max - step)/self.step_max)**2)



    # Move Function
    def move(self):
        perturbation = np.random.normal(0,self.damping,size=self.current_state) * self.t
        neighbor = self.current_state + perturbation

        for i in range(len(neighbor)):
            min_bound, max_bound = self.bounds[i]
            neighbor[i] = min(max(neighbor[i],min_bound),max_bound)
        return neighbor