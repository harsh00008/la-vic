__author__ = 'harshmalewar'

import Pyro4
import threading
import time
from order import Order, Item
import simplejson as json
import sys

class Server(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        print("Hi, my name is " + str(name) +". I'm starting my work")
        self.orders = Pyro4.Proxy("PYRONAME:lavic.server")

    def run(self):
        print("Time to work!")
        self.read_queue()
        print("I'm done. Leaving for home.")

    def read_queue(self):
        while True:
            order_json = self.orders.get_order()
            if not order_json == "":
                parsed_json = json.loads(order_json)
                message_type = parsed_json['messageType']
                if message_type == "ORDER_COMPLETE":
                    print("Hey, this is " + self.name + " giving away the order")
                    token_number = parsed_json['order']['tokenNumber']
                    customer_name = parsed_json['order']['customerName']
                    order_details = parsed_json['order']['orderDetails']
                    print("Completed Order. Token Number: " + str(token_number))
                    itemList = []
                    for index in range(len(order_details)):
                        itemId = order_details[index]['itemId']
                        itemName = order_details[index]['itemName']
                        unitCost = order_details[index]['unitCost']
                        quantity = order_details[index]['quantity']
                        item = Item(itemId, itemName, unitCost, quantity)
                        itemList.append(item)
                    order = Order(token_number, customer_name, itemList)
                    print("Broadcasting order to customers code here...")
            time.sleep(1)

serverName = str(sys.argv[1])
if not serverName == "":
    server = Server(str(sys.argv[1]))
else:
    server = Server("John")
server.start()
