import numpy as np
from tensor import *
import copy
import timeit


class FirstChoice:
    def __init__(self,cube,function_error = 'absolute'):

        assert function_error in ['squared','absolute'], 'function error must be either squared or absolute'
        self.step = 0

        if function_error == 'absolute':
            self.square_error = False
        else:
            self.square_error = True

        self.cube = copy.deepcopy(cube)
        self.initial_value = self.cube.objective_function(square_error = self.square_error)

        self.current_state = copy.deepcopy(self.cube)
        self.current_value = self.current_state.objective_function(square_error = self.square_error)

        self.best_state = copy.deepcopy(self.current_state)
        self.best_value = self.best_state.objective_function(square_error = self.square_error)

        self.hist = []

        self.step = 0