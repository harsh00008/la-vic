__author__ = 'harshmalewar'

import Pyro4
import threading
import time

class Start(threading.Thread):
    def __init__(self):
        print("Simulating addition of orders")


    def add_orders(self):
        orders = Pyro4.Proxy("PYRONAME:lavic.server")
        print("Adding new token 12 to queue")
        json_message = '{"messageType":"ORDER_COMPLETE","message":"","order":{"tokenNumber":"12","customerName":"Harsh Malewar","orderDetails":[{"itemId":"1","itemName":"Burger","unitCost":"10.12","quantity":"1"},{"itemId":"2","itemName":"French Fries","unitCost":"5.78","quantity":"3"},{"itemId":"8","itemName":"Medium Coke","unitCost":"2.28","quantity":"2"}]}}'
        orders.add_order(json_message)
        time.sleep(5)

        print("Adding new token 14 to queue")
        json_message = '{"messageType":"ORDER_COMPLETE","message":"","order":{"tokenNumber":"14","customerName":"Omi","orderDetails":[{"itemId":"1","itemName":"Burger","unitCost":"10.12","quantity":"1"},{"itemId":"2","itemName":"French Fries","unitCost":"5.78","quantity":"3"},{"itemId":"8","itemName":"Medium Coke","unitCost":"2.28","quantity":"2"}]}}'
        orders.add_order(json_message)
        time.sleep(6)

        print("Adding new token 16 to queue")
        json_message = '{"messageType":"ORDER_COMPLETE","message":"","order":{"tokenNumber":"16","customerName":"John","orderDetails":[{"itemId":"1","itemName":"Burger","unitCost":"10.12","quantity":"1"},{"itemId":"2","itemName":"French Fries","unitCost":"5.78","quantity":"3"},{"itemId":"8","itemName":"Medium Coke","unitCost":"2.28","quantity":"2"}]}}'
        orders.add_order(json_message)
        time.sleep(7)

start = Start()
start.add_orders()







