'''
File: Order.py
Project: China_Mobile_City_Delivery
Description:
-----------
Order class.
-----------
Author: 626
Created Date: 2023-1026
'''


class Order:
    def __init__(self, date=None, quantity=0, quality=0, volumn=0, place=0, readyTime=3600*7, dueTime=3600*24, packSpeed=300, waitTime=0, spuId=None):
        self.date = date
        self.quantity = quantity
        self.quality = quality
        self.volumn = volumn
        self.place = place
        self.readyTime = readyTime
        self.dueTime = dueTime
        self.packSpeed = packSpeed
        self.waitTime = waitTime
        self.spuId = spuId   