'''
File: generate_instance.py
Project: China_Mobile_City_Delivery
Description:
-----------
generate the random instance and save it as inputs.
-----------
Author: 626
Created Date: 2023-1026
'''


import random
import json
import math
import pandas as pd
import numpy as np


class Instance:
    def __init__(self, node_num, order_num, estimateCode):
        """
        init the Instance

        Args:
            node_num (int): number of the instance's node
            order_num (int): number of the instance's order_num
            estimateCode (string): instance's name.
        """
        self.node_num = node_num
        self.order_num = order_num
        self.nodeDtoList = []
        self.truckTypeDtoList = []
        self.truckTypeMap = {}
        self.distanceMap = {}
        self.orders = []
        self.estimateCode = estimateCode
        self.generate_json_file()

    def generate_node(self):
        """ generate the node """
        for node in range(self.node_num):
            nodeDict = {}
            if node <= 9:
                nodeCode = "node0" + str(node)
            else:
                nodeCode = "node" + str(node)
            nodeDict["nodeCode"] = nodeCode
            nodeDict["mustFirst"] = False
            nodeDict["x_coords"] = random.randint(0, 10000)
            nodeDict["y_coords"] = random.randint(0, 10000)

            self.nodeDtoList.append(nodeDict)

    def generate_truck(self):
        """ generate the truckType """
        self.truckTypeDtoList = \
        [
            {
                "truckTypeId": "40001",
                "truckTypeCode": "R110",
                "truckTypeName": "20GP",
                "length": 5890.0,
                "width": 2318.0,
                "height": 2270.0,
                "maxLoad": 18000.0,
                "startPrice": 350,
                "pointPrice": 50,
                "meterPrice": 0.15,
                "speed": 65 * 1000 / 3600
            },
            {
                "truckTypeId": "41001",
                "truckTypeCode": "CT10",
                "truckTypeName": "40GP",
                "length": 11920.0,
                "width": 2318.0,
                "height": 2270.0,
                "maxLoad": 23000.0,
                "startPrice": 450,
                "pointPrice": 100,
                "meterPrice": 1.22,
                "speed": 35 * 1000 / 3600,
                "startPrice": 350,
                "pointPrice": 50,
                "meterPrice": 0.2,
                "speed": 60 * 1000 / 3600
            },
            {
                "truckTypeId": "42001",
                "truckTypeCode": "CT03",
                "truckTypeName": "40HQ",
                "length": 11920.0,
                "width": 2318.0,
                "height": 2600.0,
                "maxLoad": 23000.0,
                "startPrice": 550,
                "pointPrice": 110,
                "meterPrice": 0.3,
                "speed": 55 * 1000 / 3600
            }
        ]
        self.truckTypeMap = \
        {
            "40001": {
                "truckTypeId": "40001",
                "truckTypeCode": "R110",
                "truckTypeName": "20GP",
                "length": 5890.0,
                "width": 2318.0,
                "height": 2270.0,
                "maxLoad": 18000.0,
                "startPrice": 350,
                "pointPrice": 50,
                "meterPrice": 0.4,
                "speed": 50 * 1000 / 3600
            },
            "41001": {
                "truckTypeId": "41001",
                "truckTypeCode": "CT10",
                "truckTypeName": "40GP",
                "length": 11920.0,
                "width": 2318.0,
                "height": 2270.0,
                "maxLoad": 23000.0,
                "startPrice": 450,
                "pointPrice": 100,
                "meterPrice": 0.5,
                "speed": 45 * 1000 / 3600
            },
            "42001": {
                "truckTypeId": "42001",
                "truckTypeCode": "CT03",
                "truckTypeName": "40HQ",
                "length": 11920.0,
                "width": 2318.0,
                "height": 2600.0,
                "maxLoad": 23000.0,
                "startPrice": 550,
                "pointPrice": 110,
                "meterPrice": 0.6,
                "speed": 40 * 1000 / 3600
            }
        }
    
    def generate_distanceMap(self):
        """ generate the distanceMap """
        # generate the node to node, include end_point.
        for node1 in range(self.node_num):
            for node2 in range(self.node_num):
                if node1 != node2:
                    name = "{}+{}".format(
                        self.nodeDtoList[node1]["nodeCode"], 
                        self.nodeDtoList[node2]["nodeCode"]
                        )
                    distance = math.sqrt(
                                        (self.nodeDtoList[node1]["x_coords"]
                                          - self.nodeDtoList[node2]["x_coords"])**2
                                        + ( 
                                        self.nodeDtoList[node1]["y_coords"]
                                          - self.nodeDtoList[node2]["y_coords"]
                                        )**2
                                        )
                    self.distanceMap[name] = distance

    def generate_orders(self):
        """ generate the orders """
        # random split the orders into node's number.
        def random_split_orders(order_num, node_num):
            partitions = sorted(random.sample(range(1, order_num), node_num - 1))
            result = [partitions[0]]
            for i in range(1, node_num - 1):
                result.append(partitions[i] - partitions[i - 1])
            result.append(order_num - partitions[-1])
            return result
        if self.node_num == 1:
            if self.node_num == 1:
                orderInEachNode = [self.order_num]
        else:
            orderInEachNode = random_split_orders(self.order_num, self.node_num-1)
        # generate random orders for each node.
        order_num = 0
        for node in range(1, self.node_num):
            for order in range(orderInEachNode[node-1]):
                orderInfo = {}
                orderInfo["spuId"] = str(order_num)
                order_num += 1
                orderInfo["nodeCode"] = self.nodeDtoList[node]["nodeCode"]
                orderInfo["quantity"] = random.randint(1, 10)
                orderInfo["length"] = random.randint(5,15)*100
                orderInfo["width"] = random.randint(4,12)*100
                orderInfo["height"] = random.randint(3,9)*100
                orderInfo["volumes"] = (orderInfo["height"]*orderInfo["width"]*orderInfo["length"])
                orderInfo["weight"] = random.randint(10,40)
                orderInfo["readyTime"] = 7 * 3600
                orderInfo["dueTime"] = 17 * 3600
                orderInfo["packSpeed"] = 3000
                orderInfo["waitTime"] = 0
                self.orders.append(orderInfo)

    def generate_json_file(self):
        """ generate the instance's json file """
        json_file = {}
        estimateCode = self.estimateCode
        algorithmBaseParamDto = {}
        # generate the node, truck, orders.
        self.generate_node()
        self.generate_truck()
        self.generate_distanceMap()
        self.generate_orders()
        # generate the json file.
        algorithmBaseParamDto["nodeDtoList"] = self.nodeDtoList
        algorithmBaseParamDto["truckTypeDtoList"] = self.truckTypeDtoList
        algorithmBaseParamDto["truckTypeMap"] = self.truckTypeMap
        algorithmBaseParamDto["distanceMap"] = self.distanceMap
        json_file["estimateCode"] = estimateCode
        json_file["algorithmBaseParamDto"] = algorithmBaseParamDto
        json_file["orders"] = self.orders
        # save into json file.
        file_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\inputs\\" + self.estimateCode
        with open(file_path, 'w') as f:
            json.dump(json_file, f, indent=4)
        # traverse json to excel.
        self.transform_json_to_excel(json_file)
    
    def transform_json_to_excel(self, json_file):
        """ transform json file to excel file """
        excel_file_path = "D:\\Desktop\\python_code\\China_Mobile_City_Delivery\\inputs\\" + self.estimateCode + '.xlsx'
        all_name = []
        all_df = []
        # create node
        node_list = json_file["algorithmBaseParamDto"]["nodeDtoList"]
        node_df = pd.DataFrame(node_list)
        node_sheet_name = '厅店'
        all_name.append(node_sheet_name)
        all_df.append(node_df)
        # create truck
        truck_list = json_file["algorithmBaseParamDto"]["truckTypeDtoList"]
        truck_df = pd.DataFrame(truck_list)
        truck_sheet_name = '车型'
        all_name.append(truck_sheet_name)
        all_df.append(truck_df)
        # create distance
        distance_matrix = self.nodes_to_distance_matrix(node_list)
        node_codes = [node['nodeCode'] for node in node_list]
        distance_df = pd.DataFrame(distance_matrix, index=node_codes, columns=node_codes)
        distance_sheet_name = '距离'
        all_name.append(distance_sheet_name)
        all_df.append(distance_df)
        # create order
        order_list = json_file["orders"]
        order_df = pd.DataFrame(order_list)
        order_sheet_name = '订单'
        all_name.append(order_sheet_name)
        all_df.append(order_df)
        # save all info.
        with pd.ExcelWriter(excel_file_path) as writer:
            for i in range(len(all_df)):
                df = all_df[i]
                sheet_name = all_name[i]
                df.to_excel(writer, sheet_name=sheet_name, index=False)

    def calculate_distance(self, node1, node2):
        # 计算两个节点之间的欧氏距离
        x1, y1 = node1['x_coords'], node1['y_coords']
        x2, y2 = node2['x_coords'], node2['y_coords']
        distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        return distance
    
    def nodes_to_distance_matrix(self, nodes):
        num_nodes = len(nodes)
        distance_matrix = [[0] * num_nodes for _ in range(num_nodes)]
        for i in range(num_nodes):
            for j in range(i, num_nodes):
                distance = self.calculate_distance(nodes[i], nodes[j])
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance  # 距离矩阵是对称的
        return distance_matrix

        
if __name__ == "__main__":
    node_num = 15
    order_num = 100
    instance_num = 1
    for i in range(1, instance_num + 1):
        instance_name = "myInstance" + "C&G"
        instance = Instance(node_num*i, order_num*i, instance_name)

