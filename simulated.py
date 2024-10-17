'''
Simulated Annealing Module 
'''

'''
Applied simulated annealing algorithm in diagonal magic cube problem
'''

# Import Relevant Libraries
import random
from tensor import Tensor

class Simulated:

    def __init__(self,tmin=0,tmax=100,cooling_schedule='linear',alpha = None):

        # Check Parameter
        assert cooling_schedule in ['linear','quadratic'],'cooling schedule must be either linear or quadratic'
        
        # Initialization
        self.t = tmax # Moved Temperature
        self.tmin = tmin
        self.tmax = tmax
        self.cooling_schedule = cooling_schedule

        if self.cooling_schedule == 'linear':
            if alpha != None:
                self.cooling_schedule = 'linear multiplicative'







    