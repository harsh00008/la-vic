__author__ = 'Harsh Malewar'

import Queue
import threading
import time
import simplejson as json
from order import Order
from order import Item
from server_announcer import ServerAnnouncer

announcer = ServerAnnouncer(1)
class Server():

    def __init__(self, server_name):
        print("Hi, I'm your server "+ server_name +". I'm starting my work.")

        announcer.start()

    def add_completed_order(self, json_message):
        parsed_json = json.loads(json_message)
        message_type = parsed_json['messageType']
        if message_type == "ORDER_COMPLETE":
            token_number = parsed_json['order']['tokenNumber']
            customer_name = parsed_json['order']['customerName']
            order_details = parsed_json['order']['orderDetails']
            itemList = []
            for index in range(len(order_details)):
                itemId = order_details[index]['itemId']
                itemName = order_details[index]['itemName']
                unitCost = order_details[index]['unitCost']
                quantity = order_details[index]['quantity']
                item = Item(itemId, itemName, unitCost, quantity)
                itemList.append(item)
            order = Order(token_number, customer_name, itemList)
            announcer.add_orders(order)
        else:
            print("Not so good")

    def execution_speed(self, speed):
        announcer.set_speed(speed)

json_message = '{"messageType":"ORDER_COMPLETE","message":"","order":{"tokenNumber":"12","customerName":"Harsh Malewar","orderDetails":[{"itemId":"1","itemName":"Burger","unitCost":"10.12","quantity":"1"},{"itemId":"2","itemName":"French Fries","unitCost":"5.78","quantity":"3"},{"itemId":"8","itemName":"Medium Coke","unitCost":"2.28","quantity":"2"}]}}'
server = Server("Harsh")
server.add_completed_order(json_message)
json_message = '{"messageType":"ORDER_COMPLETE","message":"","order":{"tokenNumber":"15","customerName":"Harsh Malewar","orderDetails":[{"itemId":"1","itemName":"Burger","unitCost":"10.12","quantity":"1"},{"itemId":"2","itemName":"French Fries","unitCost":"5.78","quantity":"3"},{"itemId":"8","itemName":"Medium Coke","unitCost":"2.28","quantity":"2"}]}}'
server.add_completed_order(json_message)
json_message = '{"messageType":"ORDER_COMPLETE","message":"","order":{"tokenNumber":"17","customerName":"Harsh Malewar","orderDetails":[{"itemId":"1","itemName":"Burger","unitCost":"10.12","quantity":"1"},{"itemId":"2","itemName":"French Fries","unitCost":"5.78","quantity":"3"},{"itemId":"8","itemName":"Medium Coke","unitCost":"2.28","quantity":"2"}]}}'
server.add_completed_order(json_message)
