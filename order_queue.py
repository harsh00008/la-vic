__author__ = 'Harsh Malewar'

import Pyro4
import Queue
import json
import socket

Pyro4.config.REQUIRE_EXPOSE = True

ordersQueue = Queue.Queue()
class OrderQueue(object):

    @Pyro4.expose
    def get_order(self):
        return ordersQueue.get()

    @Pyro4.expose
    def add_order(self, json_message):
        print("Order Ready : "+json_message['order']['tokenNumber'])
        ordersQueue.put(json_message)

    @Pyro4.expose
    def get_size(self):
        return ordersQueue.qsize()

order = OrderQueue()
myIp = str(socket.gethostbyname(socket.gethostname()))
daemon=Pyro4.Daemon(myIp)
ns=Pyro4.locateNS()
uri=daemon.register(order)
ns.register("lavic.queue.readyOrders", uri)
print("Order Queue started on : " + str(uri))
daemon.requestLoop()