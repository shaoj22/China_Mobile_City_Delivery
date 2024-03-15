'''
File: solomon.py
Project: China_Mobile_City_Delivery
Description:
-----------
solomon heuristic algorithm for the MVVRPTW problem.
-----------
Author: 626
Created Date: 2023-1026
'''


import sys
sys.path.append("..")   
import numpy as np
from entity import Graph as GraphTools
from utils.render import render_route


class Solomon_Insertion():
    def __init__(self, graph):
        """
        solomon insertion algorithm to get an initial solution for VRP
        """
        self.name = "SolomonI1"
        """ set paraments """
        self.miu = 1
        self.lamda = 1 # ps: lambda is key word
        self.alpha1 = 1
        self.alpha2 = 0
        self.init_strategy = 3

        """ read data and preprocess """
        self.graph = graph
        default_vi = min(3, graph.vehicleTypeNum-1) # set default vi 
        self.weightCapacity = graph.weightCapacity[default_vi]
        self.volumnCapacity = graph.volumnCapacity[default_vi]

    def get_init_node(self, point_list):
        if self.init_strategy == 0: # 0: choose farthest
            max_d = 0
            for p in point_list:
                dist = self.graph.disMatrix[0, p]
                start_time = max(dist/self.graph.speed, self.graph.readyTime[p])
                if start_time > self.graph.dueTime[p]: # exclude point break time constraint
                    continue
                if dist > max_d:
                    max_d = dist
                    best_p = p # farthest point as max_pi
        elif self.init_strategy == 1: # 1: choose nearest
            min_d = np.inf
            for p in point_list:
                dist = self.graph.disMatrix[0, p]
                start_time = max(dist/self.graph.speed, self.graph.readyTime[p])
                if start_time > self.graph.dueTime[p]: # exclude point break time constraint
                    continue
                if dist < min_d:
                    min_d = dist
                    best_p = p # farthest point as max_pi
        elif self.init_strategy == 2: # 2: random select
            best_p = point_list[np.random.randint(len(point_list))]
        elif self.init_strategy == 3: # 3: highest due_time
            max_t = 0
            for p in point_list:
                due_time = self.graph.dueTime[p]
                start_time = max(self.graph.disMatrix[0, p]/self.graph.speed, self.graph.readyTime[p])
                if start_time > due_time: # exclude point break time constraint
                    continue
                if due_time > max_t:
                    max_t = due_time
                    best_p = p # farthest point as max_pi
        elif self.init_strategy == 4: # 4: highest start_time
            max_t = 0
            for p in point_list:
                due_time = self.graph.dueTime[p]
                start_time = max(self.graph.disMatrix[0, p]/self.graph.speed, self.graph.readyTime[p])
                if start_time > due_time: # exclude point break time constraint
                    continue
                if start_time > max_t:
                    max_t = start_time
                    best_p = p # farthest point as max_pi
        return best_p

    def run(self):
        """ construct a route each circulation """
        unassigned_points = list(range(1, self.graph.nodeNum)) 
        routes = []
        while len(unassigned_points) > 0: 
            # initiate load, point_list
            weight_load = 0
            volumn_load = 0
            point_list = unassigned_points.copy() # the candidate point set
            route_start_time_list = [0] # contains time when service started each point
            # choose the farthest point as s
            best_p = self.get_init_node(point_list)
            best_start_time = max(self.graph.disMatrix[0, best_p]/self.graph.speed, self.graph.readyTime[best_p])
            route = [0, best_p] # route contains depot and customer points 
            route_start_time_list.append(best_start_time) 
            point_list.remove(best_p) 
            unassigned_points.remove(best_p)
            weight_load += self.graph.weight[best_p]
            volumn_load += self.graph.volumn[best_p]

            """ add a point each circulation """
            while len(point_list) > 0:
                c2_list = [] # contains the best c1 value
                best_insert_list = [] # contains the best insert position
                # find the insert position with lowest additional distance
                pi = 0
                while pi < len(point_list):
                    u = point_list[pi]
                    # remove if over load
                    if weight_load + self.graph.weight[u] >= self.weightCapacity \
                       or volumn_load + self.graph.volumn[u] >= self.volumnCapacity: 
                        point_list.pop(pi)
                        continue
                    
                    best_c1 = np.inf 
                    for ri in range(len(route)):
                        i = route[ri]
                        if ri == len(route)-1:
                            rj = 0
                        else:
                            rj = ri+1
                        j = route[rj]
                        # c11 = diu + dui - miu*dij
                        c11 = self.graph.disMatrix[i, u] + self.graph.disMatrix[u, j] - self.miu * self.graph.disMatrix[i, j]
                        # c12 = bju - bj 
                        bj = route_start_time_list[rj]
                        bu = max(route_start_time_list[ri] + self.graph.serviceTime[i] + self.graph.disMatrix[i, u]/self.graph.speed, self.graph.readyTime[u])
                        bju = max(bu + self.graph.serviceTime[u] + self.graph.disMatrix[u, j]/self.graph.speed, self.graph.readyTime[j])
                        c12 = bju - bj

                        # remove if over time window
                        if bu > self.graph.dueTime[u] or bju > self.graph.dueTime[j]:
                            continue
                        PF = c12
                        pf_rj = rj
                        overtime_flag = 0
                        while PF > 0 and pf_rj < len(route)-1:
                            pf_rj += 1
                            bju = max(bju + self.graph.serviceTime[route[pf_rj-1]] + self.graph.disMatrix[route[pf_rj-1], route[pf_rj]], \
                                self.graph.readyTime[route[pf_rj]]) # start time of pf_rj
                            if bju > self.graph.dueTime[route[pf_rj]]:
                                overtime_flag = 1
                                break
                            PF = bju - route_start_time_list[pf_rj] # time delay
                        if overtime_flag == 1:
                            continue

                        # c1 = alpha1*c11(i,u,j) + alpha2*c12(i,u,j)
                        c1 = self.alpha1*c11 + self.alpha2*c12
                        # find the insert pos with best c1
                        if c1 < best_c1:
                            best_c1 = c1
                            best_insert = ri+1
                    # remove if over time (in all insert pos)
                    if best_c1 == np.inf:
                        point_list.pop(pi)
                        continue
                    c2 = self.lamda * self.graph.disMatrix[0, u] - best_c1
                    c2_list.append(c2)
                    best_insert_list.append(best_insert)
                    pi += 1
                if len(point_list) == 0:
                    break
                # choose the best point
                best_pi = np.argmax(c2_list)
                best_u = point_list[best_pi]
                best_u_insert = best_insert_list[best_pi] 
                # update route
                route.insert(best_u_insert, best_u)
                point_list.remove(best_u)
                unassigned_points.remove(best_u) # when point is assigned, remove from unassigned_points
                weight_load += self.graph.weight[best_u]
                volumn_load += self.graph.volumn[best_u]
                # update start_time
                start_time = max(route_start_time_list[best_u_insert-1] + self.graph.serviceTime[route[best_u_insert-1]] + self.graph.disMatrix[route[best_u_insert-1], best_u]/self.graph.speed, self.graph.readyTime[best_u])
                route_start_time_list.insert(best_u_insert, start_time)
                for ri in range(best_u_insert+1, len(route)):
                    start_time = max(route_start_time_list[ri-1] + self.graph.serviceTime[route[ri-1]] + self.graph.disMatrix[route[ri-1], route[ri]]/self.graph.speed, self.graph.readyTime[route[ri]])
                    route_start_time_list[ri] = start_time
            route.append(0)
            routes.append(route) 

        return routes

if __name__ == "__main__":
    input_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\inputs\\myInstance1"
    graph = GraphTools.Graph(input_path=input_path)
    alg = Solomon_Insertion(graph)
    routes = alg.run()
    print(routes)
    render_route(graph.location, routes)

 