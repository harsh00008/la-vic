import Pyro4
import time
import json
import sys
import socket
from colorama import init, Fore, Back, Style
import threading
import thread


Pyro4.config.REQUIRE_EXPOSE = True

class Server(object):
    my_uri = ""
    def __init__(self, name):
        init()
        self.clear_screen()
        self.queue_address = "PYRONAME:lavic.queue.readyOrders"
        self.print_main_title("NEW SERVER " + str(name).upper())
        self.server_name = name
        self.print_info("Hi, my name is " + str(self.server_name) +". I'm starting my work")
        try:
            self.print_network("Connecting to " + str(self.queue_address) + "...")
            self.orders = Pyro4.Proxy(self.queue_address)
            self.ns=Pyro4.locateNS()
            self.print_success("Connected to " + str(self.queue_address))
        except:
            self.print_error("Some problem connecting to queue. Exiting...")
            exit()
        self.order_json = None
        self.address = None

    def run(self):
        self.print_success("Time to work!")
        server_name = self.server_name
        while True:
            try:
                if int(self.orders.get_size()) > 0:
                    parsed_json = self.orders.get_order()
                    if parsed_json is not None:
                        message_type = parsed_json['messageType']
                        if message_type == "ORDER_COMPLETE":
                            token_number = parsed_json['order']['tokenNumber']
                            self.print_title("Announcing token "+ str(token_number))
                            parsed_json['messageType'] = "ORDER_PREPARED"
                            self.order_json = parsed_json
                            self._broadcast_customers()
                time.sleep(6)
            except:
                self.print_error("Some problem getting json")

    @Pyro4.expose
    def take_order(self):
        self.print_title("Hey! Thanks. Please take your order!")
        response_json = self.order_json
        self.order_json = None
        return response_json

    def _broadcast_customers(self):
        count = 0
        customer_list = self.ns.list("lavic.customer.")
        shout_limit = 3
        try:
            for count in range(0, shout_limit):
                if self.order_json is not None:
                    token_number = str(self.order_json['order']['tokenNumber'])
                    self.print_info("Token number " + token_number + " Please take your order - Announcement: " + str(count + 1))
                    for customer in customer_list:
                        pyro_address = customer_list[customer]
                        self._print_network("Announcing tokens to " + str(customer) + " : " + pyro_address)
                        try:
                            customer_obj = Pyro4.Proxy(pyro_address)
                            customer_obj.listen("server", self.address, self.order_json )
                            self.print_success("Sent")
                        except:
                            self.print_error("Some problem connecting to customers :" + str(customer))
                else:
                    self.order_json = None
                    return
                time.sleep(1)
        except:
            print("Some Problem in broadcast")
        finally:
            self.print_info("No takers. Sorry, disposing order.")
            return

    def set_my_pyro(self, address):
        self.print_success("Setting my address: " + address)
        self.address = address

    def print_success(self, message):
        print(Back.GREEN + Style.BRIGHT  +  Fore.BLACK + " SUCCESS " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def print_info(self, message):
        print(Back.BLUE + Style.BRIGHT  +  Fore.WHITE + " INFO " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def print_error(self, message):
        print( Back.RED + Style.BRIGHT  +  Fore.WHITE + " ERROR " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def print_network(self, message):
        print( Back.YELLOW + Style.BRIGHT  +  Fore.BLACK + " NETWORK " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def print_title(self, message):
        print(Fore.GREEN + Style.BRIGHT)
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print("                 " + str(message))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def print_main_title(self, message):
        print(Fore.CYAN + Back.WHITE + Style.BRIGHT)
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(Back.RESET)
        print( "                        " + str(message).upper()+ "                     ")
        print(Back.WHITE)
        print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)

    def clear_screen(self):
        print("\033c")

class ActivateThread (threading.Thread):
    def __init__(self, server):
        threading.Thread.__init__(self)
        self.server = server
    def run(self):
        activate(self.server)

def activate(server):
    myIp = str(socket.gethostbyname(socket.gethostname()))
    daemon=Pyro4.Daemon(myIp)                 # make a Pyro daemon
    ns=Pyro4.locateNS()
    uri=daemon.register(server)
    server.set_my_pyro(str(uri))
    daemon.requestLoop()

if __name__ == "__main__":
    try:
        serverName = str(sys.argv[1])
    except:
        print(Back.RED + Style.BRIGHT + Fore.WHITE  + " ERROR " + Fore.RESET + Back.RESET + Style.RESET_ALL + Fore.MAGENTA + Style.BRIGHT + " : Please specify a server name as an argument. Exiting...")
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)
        exit()

    server = Server(serverName)
    activateThread = ActivateThread(server)
    activateThread.start()
    server.print_success("Running server now")
    server.run()





