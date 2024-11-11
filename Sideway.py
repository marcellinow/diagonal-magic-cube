import numpy as np
from tensor import *
import copy
import timeit

class Sideway:
    def __init__(self,cube,max_sideway_move = 100,function_error = 'absolute'):


        if function_error == 'absolute':
            self.square_error = False
        else:
            self.square_error = True

        self.cube = copy.deepcopy(cube)
        self.initial_value = self.cube.objective_function(square_error = self.square_error)

        self.current_state = copy.deepcopy(self.cube)
        self.current_value = self.cube.objective_function(square_error = self.square_error)
    
        self.best_state = copy.deepcopy(self.current_state)
        self.best_value = self.best_state.objective_function(square_erorr = self.square_error)

        self.hist = []

        self.step = 0
        self.sideway_ctr = 0

        isTerminate = True
        self.start_time = timeit.default_timer()
        print(f"initial value: {self.initial_value}\n")
        while isTerminate:
            
            neighbors= self.bestNeighbors()
            if (self.best_value == 0) or neighbors is None:
                self.end_time = timeit.default_timer()
                # print('ke first ifelse\n')
                break

            self.step +=1
            neighbor_value = neighbors.objective_function(square_error = self.square_error)
            self.hist.append([self.step, self.current_value])

            print(50*"- -")
            print(f"step {self.step} ; best successor value: {neighbor_value} ; current value: {self.current_value}")
            print(50*"- -")

            if neighbor_value == self.current_value:
                self.sideway_ctr += 1
                self.sideway_step = 0
                while (self.sideway_step < max_sideway_move):
                    choosen_neighbor = self.move()
                    choosen_value = choosen_neighbor.objective_function()
                    if choosen_value < self.current_value:
                        self.best_state = choosen_neighbor
                        self.current_value = choosen_value
                        break
                    self.sideway_step += 1
            elif neighbor_value < self.current_value:
                self.best_state = copy.deepcopy(neighbors)
                self.best_value = neighbor_value
                self.current_state = copy.deepcopy(neighbors)
                self.current_value = neighbor_value
            else:
                isTerminate = True
        
            self.hist.append([
                self.step,
                self.sideway_ctr,
                
            ])
            
    def move(self,state):
        shape = self.cube.shape
        moved_cube = copy.deepcopy(state)
        p0 = (np.random.randint(0,shape[0]),
              np.random.randint(0,shape[1]),
              np.random.randint(0,shape[2]))
        p1 = p0
        while p1  == p0:
            p1 = (np.random.randint(0,shape[0]),
              np.random.randint(0,shape[1]),
              np.random.randint(0,shape[2]))
        moved_cube.array[p0], moved_cube.array[p1] = moved_cube.array[p1], moved_cube.array[p0]
        return moved_cube
    
    def bestNeighbors(self):
        first_neighbor = copy.deepcopy(self.current_state)
        first_neighbor = self.move(first_neighbor)
        best_value = first_neighbor.objective_function()
        n = self.cube.max_len() ** 2
        
        num_neighbors = int((n * (n-1))/2)

        for _ in range(num_neighbors):
            candidate = copy.deepcopy(first_neighbor)
            candidate = self.move(candidate)
            candidate_value = candidate.objective_function(square_error = self.square_error)

            if candidate_value <= best_value:
                best_neighbor = candidate
                best_value = candidate_value

        return best_neighbor if best_neighbor else None