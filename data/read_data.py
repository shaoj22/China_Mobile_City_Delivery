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


import sys
sys.path.append("..")
import json
import numpy as np
import re
from entity.Order import Order
from entity.Node import Node
from entity.Map import Map
from entity.Vehicle import Vehicle


class Data():
    def __init__(self, input_path):
        """ 
        init of the Data
        
        Args:
            input_path (str): file path of the inputs.
        """
        self.input_path = input_path
        map, order_list, vehicle_type_list = read_data(self.input_path)
        self.map = map
        self.vehicle_type_list = vehicle_type_list
        self.order_list = order_list

def read_data(input_path):
    """ read data from inputs """
    with open(input_path, 'r') as f:
        j = json.load(f)
        tempDict = j['algorithmBaseParamDto']
    nodeDtoList = tempDict['nodeDtoList']
    truckTypeDtoList = tempDict['truckTypeDtoList']
    distanceMap = tempDict['distanceMap']
    orders = j['orders']
    # generate Map
    node_list = []
    for node in range(len(nodeDtoList)):
        posX = nodeDtoList[node]['x_coords']
        posY = nodeDtoList[node]['y_coords']
        address = nodeDtoList[node]['nodeCode']
        node = Node(posX, posY, address)
        node_list.append(node)
    disMatrix = np.zeros((len(node_list), len(node_list)))
    for i in range(len(node_list)):
        for j in range(len(node_list)):
            if i == j:
                disMatrix[i][j] = 0
                continue
            name = node_list[i].address + "+" + node_list[j].address
            disMatrix[i][j] = distanceMap[name]
    map = Map(node_list, disMatrix)
    # generate Order
    order_list = []
    for i in range(len(orders)):
        date = None
        quantity = orders[i]['quantity']
        weight = orders[i]['weight']
        volumes = orders[i]['volumes']
        pattern = r"node(\d+)"
        match = re.match(pattern, orders[i]["nodeCode"])
        number = int(match.group(1))
        place = int(number)
        readyTime = orders[i]['readyTime']
        dueTime = orders[i]['dueTime']
        packSpeed = orders[i]['packSpeed']
        waitTime = orders[i]['waitTime']
        spuId = orders[i]['spuId']
        order = Order(date, quantity, weight, volumes, place, readyTime, dueTime, packSpeed, waitTime, spuId)
        order_list.append(order)
    # generate Truck
    vehicle_type_list = []
    for i in range(len(truckTypeDtoList)):
        truckTypeName = truckTypeDtoList[i]['truckTypeName']
        truckWeight = truckTypeDtoList[i]['maxLoad']
        truckVolumes = truckTypeDtoList[i]['length']*truckTypeDtoList[i]['width']*truckTypeDtoList[i]['height']
        startPrice = int(truckTypeDtoList[i]['startPrice'])
        pointPrice = int(truckTypeDtoList[i]['pointPrice'])
        meterPrice = float(truckTypeDtoList[i]['meterPrice'])
        speed = truckTypeDtoList[i]['speed']
        vehicle_type = Vehicle(truckTypeName, truckWeight, truckVolumes, startPrice, pointPrice, meterPrice, speed)
        vehicle_type_list.append(vehicle_type)
    return map, order_list, vehicle_type_list


if __name__ == "__main__":
    input_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\inputs\\myInstance2"
    instance = Data(input_path)
    
    
    
        
    
