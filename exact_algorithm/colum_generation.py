'''
File: colum_generation.py
Project: China_Mobile_City_Delivery
Description:
-----------
C&G algorithm.
-----------
Author: 626
Created Date: 2023-1026
'''


import sys
sys.path.append("..")
from exact_algorithm.branch_and_price import *
from entity import Graph as GraphTools


class ColumnGeneration(BranchAndPrice):
    def __init__(self, graph):
        self.name = "CG"
        # graph info
        self.graph = graph
        self.global_column_pool = {}
        # build and set RLMP, SP
        self.RLMP = self.set_RLMP_model(graph)
        self.SP = self.set_SP_model(graph)    
        # create nodes
        self.root_node = BPNode(graph, self.RLMP, self.SP, self.global_column_pool)
        self.incumbent_node = self.root_node
        self.current_node = self.root_node
        # set strategies
        self.branch_strategy = "max_inf"
        self.search_strategy = "best_LB_first"
        # algorithm part
        self.node_list = []
        self.global_LB = np.inf
        self.global_UB = -np.inf
        # display parament
        self.iter_cnt = 0
        self.Gap = np.inf
        self.fea_sol_cnt = 0
        self.BP_tree_size = 0
        self.branch_var_name = ""

    def run(self):
        self.root_init()
        return self.get_routes(self.incumbent_node)

if __name__ == "__main__":
    # column generation
    input_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\inputs\\myInstanceC&G"
    graph = GraphTools.Graph(input_path=input_path)    
    alg = ColumnGeneration(graph)
    alg.run() # run CG
    alg.show_result()

