import sys
sys.path.append("..")
from entity import Graph as GraphTools
from mate_heuristic_algorithm.ALNS import ALNS
from data.output_result import output_result


instance_num = 10
for i in range(1, instance_num+1):
    input_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\inputs\\"\
          + "myInstance" + str(i)
    graph = GraphTools.Graph(input_path=input_path)
    iter_num = 50000
    alg = ALNS(graph, iter_num, heuristic=None)
    routes = alg.run()
    output_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\outputs\\"\
          + "outputs-myInstance" + str(i)
    alg.show_result()
    alg.show_process(output_path+"iteration-chart")
    alg.show_routes(output_path+"visualization-chart")
    output_name = "outputs-myInstance" + str(i) 
    output_result(graph, routes, output_name)