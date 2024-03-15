'''
File: ALNS.py
Project: China_Mobile_City_Delivery
Description:
-----------
VNS mate-heuristic algorithm for the MVVRPTW problem.
-----------
Author: 626
Created Date: 2023-1026
'''


import sys
sys.path.append("..")
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from tqdm import trange, tqdm
import math
from entity import Graph as GraphTools
from heuristic_algorithm.solomon_insertion import Solomon_Insertion
from data.output_result import output_result


# neighbour stuctures (operators)
class Relocate():
    def __init__(self, k=1):
        self.k = k # how many points relocate together, k=1:relocate, k>1:Or-Opt

    def run(self, solution):
        """relocate point and the point next to it randomly inter/inner route (capacity not considered)+

        Args:
            solution (List[int]): idxs of points of each route (route seperate with idx 0)

        Returns:
            neighbours (List[List[int]]): idxs of points of each route (seperate with idx 0) of each neighbour 
        """
        neighbours = []
        # 1. choose a point to relocate
        for pi in range(1, len(solution)-self.k):
            # 2. choose a position to put
            for li in range(1, len(solution)-self.k): # can't relocate to start/end
                neighbour = solution.copy()
                points = []
                for _ in range(self.k):
                    points.append(neighbour.pop(pi))
                for p in points[::-1]:
                    neighbour.insert(li, p)
                neighbours.append(neighbour)
        return neighbours     

    def get(self, solution):
        pi = np.random.randint(1, len(solution)-self.k)
        li = np.random.randint(1, len(solution)-self.k)
        neighbour = solution.copy()
        points = []
        for _ in range(self.k):
            points.append(neighbour.pop(pi))
        for p in points[::-1]:
            neighbour.insert(li, p)
        assert len(neighbour) == len(solution)
        return neighbour

class Exchange():
    def __init__(self, k=1):
        self.k = k # how many points exchange together

    def run(self, solution):
        """exchange two points randomly inter/inner route (capacity not considered)
        ps: Exchange operator won't change the points number of each vehicle

        Args:
            solution (List[int]): idxs of points of each route (route seperate with idx 0)

        Returns:
            neighbours (List[List[int]]): idxs of points of each route (seperate with idx 0) of each neighbour 
        """
        neighbours = []
        # 1. choose point i
        for pi in range(1, len(solution)-2*self.k-1):
            # 2. choose point j
            for pj in range(pi+self.k+1, len(solution)-self.k): 
                # if math.prod(solution[pi:pi+self.k]) == 0 or math.prod(solution[pj:pj+self.k]) == 0: # don't exchange 0
                #     continue
                neighbour = solution.copy()
                tmp = neighbour[pi:pi+self.k].copy()
                neighbour[pi:pi+self.k] = neighbour[pj:pj+self.k]
                neighbour[pj:pj+self.k] = tmp
                neighbours.append(neighbour)
        return neighbours    

    def get(self, solution):
        pi = np.random.randint(1, len(solution)-2*self.k-1)
        pj = np.random.randint(pi+self.k+1, len(solution)-self.k)
        while math.prod(solution[pi:pi+self.k]) == 0 or math.prod(solution[pj:pj+self.k]) == 0: # don't exchange 0
            pi = np.random.randint(1, len(solution)-2*self.k-1)
            pj = np.random.randint(pi+self.k+1, len(solution)-self.k)
        neighbour = solution.copy()
        tmp = neighbour[pi:pi+self.k].copy()
        neighbour[pi:pi+self.k] = neighbour[pj:pj+self.k]
        neighbour[pj:pj+self.k] = tmp
        assert len(neighbour) == len(solution)
        return neighbour

class Reverse():
    def __init__(self):
        pass

    def run(self, solution):
        """reverse route between two points randomly inter/inner route (capacity not considered)

        Args:
            solution (List[int]): idxs of points of each route (route seperate with idx 0)

        Returns:
            neighbours (List[List[int]]): idxs of points of each route (seperate with idx 0) of each neighbour 
        """
        neighbours = []
        # 1. choose point i
        for pi in range(1, len(solution)-2):
            # 2. choose point j
            for pj in range(pi+1, len(solution)-1): 
                neighbour = solution.copy()
                neighbour[pi:pj+1] = neighbour[pj:pi-1:-1]
                neighbours.append(neighbour)
        return neighbours 
    
    def get(self, solution):
        pi = np.random.randint(1, len(solution)-2)
        pj = np.random.randint(pi+1, len(solution)-1)
        neighbour = solution.copy()
        neighbour[pi:pj+1] = neighbour[pj:pi-1:-1]
        assert len(neighbour) == len(solution)
        return neighbour

# Variable Neighbourhood Search Algorithm
class VNS():
    def __init__(self, graph, iter_num=100000, heuristic=None):
        self.name = "VNS"
        self.graph = graph
        self.iter_num = iter_num 
        self.heuristic = heuristic
        # paraments for VNS
        self.operators_list = [Reverse(), Relocate(), Exchange()]
        # for k in range(3, 10):
        #     self.operators_list.append(Relocate(k))
        #     self.operators_list.append(Exchange(k))
        # display paraments
        self.process = []

    def solution_init(self):
        """
        generate initial solution randomly
        """
        if self.heuristic is not None:
            alg = self.heuristic(self.graph) 
            routes = alg.run()
            solution = [0]
            for route in routes:
                solution += route[1:]
        else:
            # all smallest vehicle
            vi = 0
            weight_capacity = self.graph.weightCapacity[vi]
            volumn_capacity = self.graph.volumnCapacity[vi]
            point_list = list(range(1, self.graph.nodeNum))
            np.random.shuffle(point_list)
            solution = [0]
            weight_sum = 0
            volumn_sum = 0
            for i in range(len(point_list)):
                pi = point_list[i]
                point_weight = self.graph.weight[pi]
                point_volumn = self.graph.volumn[pi]
                if weight_sum + point_weight < weight_capacity and \
                volumn_sum + point_volumn < volumn_capacity:
                    solution.append(pi)
                    weight_sum += point_weight
                    volumn_sum += point_volumn
                else:
                    solution.append(0)
                    solution.append(pi)
                    weight_sum = point_weight
                    volumn_sum = point_volumn
            solution.append(0) # add last 0
        self.best_solution = solution
        self.best_obj = self.cal_objective(solution)
        return solution
    
    def transfer(self, solution):
        """
        transfer solution to routes
        """
        routes = []
        for i, p in enumerate(solution[:-1]): # pass the end 0
            if p == 0:
                if i > 0:
                    routes[-1].append(0) # add end 0
                routes.append([0]) # add start 0
            else:
                routes[-1].append(p)
        else:
            routes[-1].append(0) # add final 0
        return routes
                
    def cal_objective(self, solution):
        """ calculate fitness(-obj) 
        obj = distance_cost + overload_cost + overtime_cost
        """
        routes = self.transfer(solution)
        obj = self.graph.cal_objective(routes) 
        return obj

    def get_neighbours(self, solution, operator):
        neighbours = operator.run(solution)
        return neighbours
    
    def choose_neighbour(self, neighbours):
        chosen_ni = np.random.randint(len(neighbours))
        return chosen_ni
        
    def remove_empty_vehicle(self, solution):
        idx = 1
        while idx < len(solution):
            if solution[idx-1] == 0 and solution[idx] == 0:
                solution.pop(idx)
            else:
                idx += 1
        return solution

    def show_result(self):
        self.best_routes = self.transfer(self.best_solution)
        print("Optimal Obj = {}".format(self.best_obj)) 
        vehicle_chosen = np.zeros(self.graph.vehicleTypeNum) # count number of each vehicle
        over_load_num = 0
        over_time_num = 0
        for ri in range(len(self.best_routes)):
            route = self.best_routes[ri]
            if len(route) <= 2:
                continue
            vi = self.graph.choose_vehicle(route)
            if vi is None:
                over_load_num += 1
            else:
                vehicle_chosen[vi] += 1
            tw_cost = self.graph.cal_time_window_cost(route)
            if tw_cost > 0:
                over_time_num += 1
        print("Vehicle:")
        for vi in range(self.graph.vehicleTypeNum):
            vehicleType = self.graph.vehicleTypeName[vi]
            vehicleNum = vehicle_chosen[vi]
            print("  {}: {}".format(vehicleType, vehicleNum))
        print("Overload {} routes, overtime {} routes".format(over_load_num, over_time_num))

    def show_process(self, output_path):
        y = self.process
        x = np.arange(len(y))
        plt.plot(x, y)
        plt.savefig(output_path)
        # plt.show()
        plt.close() 

    def show_routes(self, output_path):
        self.best_routes = self.transfer(self.best_solution)
        self.graph.visualize_route(self.graph.location,self.best_routes, output_path)

    def run(self):
        self.solution_init() # solution in form of routes
        neighbours = self.get_neighbours(self.best_solution, operator=self.operators_list[0])
        operator_k = 0
        for step in trange(self.iter_num):
            ni = self.choose_neighbour(neighbours)
            cur_solution = neighbours[ni]
            cur_solution = self.remove_empty_vehicle(cur_solution)
            cur_obj = self.cal_objective(cur_solution)
            # obj: minimize the total distance 
            if cur_obj < self.best_obj: 
                print("1", self.operators_list)
                self.operators_list.insert(0, self.operators_list.pop(operator_k))
                print("2", self.operators_list)
                operator_k = 0
                self.best_solution = cur_solution
                self.best_obj = cur_obj
                neighbours = self.get_neighbours(self.best_solution, operator=self.operators_list[0])
            else:
                neighbours.pop(ni)
                if len(neighbours) == 0: # when the neighbour space empty, change anothor neighbour structure(operator)
                    operator_k += 1
                    if operator_k < len(self.operators_list):
                        operator = self.operators_list[operator_k]
                        neighbours = self.get_neighbours(self.best_solution, operator=operator)
                    else:
                        print('local optimal, break out, iterated {} times'.format(step))
                        break

            self.process.append(self.best_obj)
        self.best_routes = self.transfer(self.best_solution)
        return self.best_routes   


if __name__ == "__main__":
    input_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\inputs\\myInstance2"
    graph = GraphTools.Graph(input_path=input_path)    
    alg = VNS(graph, iter_num=10000, heuristic=None)
    routes = alg.run()
    print(routes)
    # alg.show_result() 
    # alg.show_process()
    # alg.show_routes()
    # output_result(graph, routes)


    
                
                




