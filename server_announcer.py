__author__ = 'harshmalewar'
import threading
import time
import Queue
from order import Order

ordersQueue = Queue.Queue()

class ServerAnnouncer(threading.Thread):

    def __init__(self, speed):
        threading.Thread.__init__(self)
        self.speed  = speed

    def set_speed(self, speed):
        self.speed = speed

    def run(self):
        print("I'm watching the queue for completed orders")
        self.watch_queue()

    def watch_queue(self):
        while True:
            if not ordersQueue.empty():
                order = ordersQueue.get()
                print("Token Number " + str(order.get_token_number()) + ", Please collect your order")
                time.sleep(1)

    def add_orders(self, order):
        ordersQueue.put(order)
        print("Added " + str(order.get_token_number()) + " to my queue")