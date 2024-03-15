'''
File: Node.py
Project: China_Mobile_City_Delivery
Description:
-----------
Node class.
-----------
Author: 626
Created Date: 2023-1026
'''


class Node:
    def __init__(self, posX, posY, address):
        self.posX = posX
        self.posY = posY
        self.address = address
    
    def copy(self):
        return Node(self.posX, self.posY, self.address)
    
    def set_order_information(self, order):
        self.date = order.date
        self.quantity = order.quantity
        self.quality = order.quality
        self.volumn = order.volumn
        self.place = order.place
        self.readyTime = order.readyTime
        self.dueTime = order.dueTime
        self.serviceTime = self.quality / order.packSpeed + order.waitTime
  

