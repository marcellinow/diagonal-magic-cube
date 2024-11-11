import numpy as np
import copy
from tensor import *
import timeit

class Steepest:

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

    
        self.start_time = timeit.default_timer()

        print(f"initial value: {self.initial_value}\n")

        while True:
            neighbors = self.bestNeighbors()
            if (self.best_value == 0) or not neighbors:
                break

            self.step += 1
            neighbor_value = neighbors.objective_function(square_error = self.square_error)
            self.hist.append([self.step, self.current_value])

            print(50*"- -")
            print(f"step {self.step} ; best successor value: {neighbor_value} ; current value: {self.current_value}")
            print(50*"- -")
            
            if neighbor_value < self.current_value:
                self.best_state = copy.deepcopy(neighbors)
                self.best_value = neighbor_value
                self.current_state = copy.deepcopy(neighbors)
                self.current_value = neighbor_value
            else:
                break
        self.end_time = timeit.default_timer()

    def results(self):
        print('+------------------------ RESULTS -------------------------+\n')
        print(f'    iterations: {self.step}\n')
        print(f'    initial Value: {self.initial_value:0.6f}\n')
        print(f'    final Value: {self.best_value:0.6f}\n')
        # print(f'    runtime: {self.end_time - self.start_time} seconds')
        print('+-------------------------- END ---------------------------+')

    def final_states(self):
        return Tensor(5,5,5,self.best_state.array)
    
    def move(self,state):
        shape = self.cube.shape
        p0 = (np.random.randint(0,shape[0]),
              np.random.randint(0,shape[1]),
              np.random.randint(0,shape[2]))
        p1 = p0
        while p1  == p0:
            p1 = (np.random.randint(0,shape[0]),
              np.random.randint(0,shape[1]),
              np.random.randint(0,shape[2]))
        moved_cube = copy.deepcopy(state)
        moved_cube.array[p0], moved_cube.array[p1] = moved_cube.array[p1], moved_cube.array[p0]
        return moved_cube
    
    def bestNeighbors(self):
        best_value = self.current_value
        best_neighbor = None

        n = self.cube.max_len() ** 2

        best_neighbor = None
        
        num_neighbors = int((n * (n-1))/2)

        for _ in range(num_neighbors):
            candidate = self.move(self.current_state)
            candidate_value = candidate.objective_function(square_error = self.square_error)

            if candidate_value <= best_value:
                best_neighbor = candidate

        return best_neighbor

    def hist_plot(self, title='Steepest Ascent Hill-Climbing Plot'):

        hist = np.array(self.hist)

        _, ax = plt.subplots(1, 1, figsize=(10, 5))

        ax.plot(hist[:, 0], hist[:, 1], linestyle='-', label='Value', color='red')
        
        ax.set_xlabel('Step')
        ax.set_ylabel('Objective Function')
        ax.set_title(title)
        ax.legend()

        plt.show()
        