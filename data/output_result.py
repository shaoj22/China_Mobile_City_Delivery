'''
File: read_data.py
Project: China_Mobile_City_Delivery
Description:
-----------
read input file and create Data class.
-----------
Author: 626
Created Date: 2023-1026
'''


import json


def output_result(graph, routes, outputs_name):
    # get orders's place
    place = []
    place.append(0)
    for order in graph.new_order_list:
        place.append(order.place)
    truckTypeList = []
    truckOrderList = []
    for route in routes:
        truckOrder = []
        # get the truckType of each route
        truckType = graph.choose_vehicle(route)
        truckTypeList.append(truckType)
        # get the orders of each route
        for node in route:
            if node == 0:
                continue
            temp_order = graph.order_pair_list[node-1]
            for order in temp_order:
                truckOrder.append(order)
        truckOrderList.append(truckOrder)
    output_file = {}
    for i in range(len(truckOrderList)):
        oneTruckSolution = {}
        oneTruckSolution['truckType'] = truckTypeList[i]
        # fix the route to real route
        real_route = transfer_route_to_real_route(place, routes[i])
        oneTruckSolution['truckRoute'] = real_route
        oneTruckSolution['truckOrder'] = truckOrderList[i]
        name = 'truck' + str(i)
        output_file[name] = oneTruckSolution
    file_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\outputs\\" + outputs_name
    with open(file_path, 'w') as f:
        json.dump(output_file, f, indent=4)

def transfer_route_to_real_route(place, route):
    real_route = []
    real_route.append(0)
    for i in range(1, len(route)):
        if place[route[i]] == real_route[-1]:
            continue
        real_route.append(place[route[i]])
    return real_route



    
    

