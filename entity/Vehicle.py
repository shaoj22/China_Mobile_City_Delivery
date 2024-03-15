'''
File: Vehicle.py
Project: China_Mobile_City_Delivery
Description:
-----------
Vehicle class.
-----------
Author: 626
Created Date: 2023-1026
'''


class Vehicle:
    def __init__(self, typeName, weight_capacity, volumn_capacity, startPrice, pointPrice, meterPrice, speed):
        self.typeName = typeName
        self.weight_capacity = weight_capacity
        self.volumn_capacity = volumn_capacity
        self.startPrice = startPrice
        self.pointPrice = pointPrice
        self.meterPrice = meterPrice
        self.speed = speed
