__author__ = 'harshmalewar'

import Pyro4
import threading
import time
from order import Order, Item
import simplejson as json
import sys
import socket

Pyro4.config.REQUIRE_EXPOSE = True

class Server(threading.Thread):

    def __init__(self, name):
        threading.Thread.__init__(self)
        print("Hi, my name is " + str(name) +". I'm starting my work")
        self.orders = Pyro4.Proxy("PYRONAME:lavic.server")
        self.ns=Pyro4.locateNS()
        self.order_json = None
        self.address = None

    def run(self):
        print("Time to work!")
        self.read_queue(self.name)
        print("I'm done. Leaving for home.")

    def read_queue(self, name):
        server_name = name
        while True:
            parsed_json = self.orders.get_order()
            if parsed_json is not None:
                message_type = parsed_json['messageType']
                if message_type == "ORDER_COMPLETE":
                    print("Hey, this is " + self.name + " giving away the order")
                    token_number = parsed_json['order']['tokenNumber']
                    print("------------------------------")
                    print("|    Announcing token "+ str(token_number) +"      |")
                    print("------------------------------")
                    parsed_json['messageType'] = "ORDER_PREPARED"
                    self.order_json = parsed_json
                    self._broadcast_customers()
            time.sleep(1)

    def _broadcast_customers(self):
        count = 0
        customer_list = self.ns.list("lavic.customer.")
        shout_limit = 3
        for count in range(0, shout_limit):
            if not self.order_json is None:
                print("Waiting... " + str(count))
                for customer in customer_list:
                    pyro_address = customer_list[customer]
                    print(str(customer) + " : " + pyro_address)
                    customer_obj = Pyro4.Proxy(pyro_address)
                    print("ORDER_JSON: " + str(self.order_json))
                    customer_obj.listen("server", str(self.address), self.order_json )
            else:
                self.order_json = None
                return
            time.sleep(5)
        print ("No takers! Disposing order. Sorry.")

    @Pyro4.expose
    def take_order(self):
        print("Dispersing order to customer. Thanks")
        self.order_json = None


    def set_my_pyro(self, address):
        self.address = address

serverName = str(sys.argv[1])
if serverName == "":
    serverName = "John"
if not serverName == "":
    server = Server(str(sys.argv[1]))
else:
    server = Server("John")

myIp = str(socket.gethostbyname(socket.gethostname()))
daemon=Pyro4.Daemon(myIp)                 # make a Pyro daemon
ns=Pyro4.locateNS()
uri=daemon.register(server)
server.set_my_pyro(uri)
ns.register("lavic.server.announcer", uri)
print("Ready. uri =" + str(uri))
server.start()
daemon.requestLoop()
