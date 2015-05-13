import Pyro4
import time
import json
import sys
import socket
from colorama import init, Fore, Back, Style
from threading import Thread


Pyro4.config.REQUIRE_EXPOSE = True

order_json=None
my_uri = ""

class Server(object):
    @Pyro4.expose
    def take_order(self):
        global order_json
        response_json = order_json
        order_json = None
        return response_json

def serverCustomer():
    print("Time to work!")
    global order_json
    while True:
        try:
            orders = Pyro4.Proxy("PYRONAME:lavic.queue.readyOrders")
            if int(orders.get_size()) > 0:
                parsed_json = orders.get_order()
                if parsed_json is not None:
                    message_type = parsed_json['messageType']
                    if message_type == "ORDER_COMPLETE":
                        print_info("I've got an order to announce")
                        token_number = parsed_json['order']['tokenNumber']
                        print_title("Announcing token "+ str(token_number))
                        parsed_json['messageType'] = "ORDER_PREPARED"
                        order_json = parsed_json
                        broadcast_customers()
            time.sleep(6)
        except:
            print_error("Some problem getting json")

def broadcast_customers():
        global my_uri
        global order_json

        ns=Pyro4.locateNS()
        customer_list = ns.list("lavic.customer.")
        print(str(customer_list))
        shout_limit = 3
        count = 0
        for count in range(0, shout_limit):
            if not order_json is None:
                token_number = str(order_json['order']['tokenNumber'])
                print_info("Token number " + token_number + " Please take your order - Announcement: " + str(count + 1))
                for customer in customer_list:
                    pyro_address = customer_list[customer]
                    print_network("Announcing tokens to " + str(customer) + " : " + pyro_address)
                    try:
                        global my_uri
                        customer_obj = Pyro4.Proxy(pyro_address)
                        customer_obj.listen("server", my_uri, order_json )
                        print_success("Sent")
                    except:
                        print_error("Some problem connecting to customers :" + str(customer))
            else:
                order_json = None
                return
            time.sleep(1)
        print_info("No takers. Sorry, disposing order.")

def print_success( message):
    print(Back.GREEN + Style.BRIGHT  +  Fore.BLACK + " SUCCESS " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_info( message):
    print(Back.BLUE + Style.BRIGHT  +  Fore.WHITE + " INFO " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_error( message):
    print( Back.RED + Style.BRIGHT  +  Fore.WHITE + " ERROR " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_network( message):
    print( Back.YELLOW + Style.BRIGHT  +  Fore.BLACK + " NETWORK " + Fore.RESET + Back.RESET + Style.RESET_ALL +  Fore.WHITE + Style.BRIGHT + " : " + str(message))
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_title(message):
    print(Fore.GREEN + Style.BRIGHT)
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print("                 " + str(message))
    print("- - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def print_main_title(message):
    print(Fore.CYAN + Back.WHITE + Style.BRIGHT)
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print(Back.RESET)
    print( "                        " + str(message).upper()+ "                     ")
    print(Back.WHITE)
    print("= = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =")
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)

def clear_screen():
    print("\033c")


def activate():
    serverName = str(sys.argv[1])
    server = Server()
    myIp = str(socket.gethostbyname(socket.gethostname()))
    daemon=Pyro4.Daemon(myIp)           
    ns=Pyro4.locateNS()
    uri=daemon.register(server)
    global my_uri
    my_uri = uri
    daemon.requestLoop()

if __name__ == "__main__":
    try:
        
        server_activate = Thread(target=activate)
        server_start = Thread(target=serverCustomer)
        server_start.start()
        server_activate.start()
        server_activate.join()
        server_start.join()

    except:
        print(Back.RED + Style.BRIGHT + Fore.WHITE  + " ERROR " + Fore.RESET + Back.RESET + Style.RESET_ALL + Fore.MAGENTA + Style.BRIGHT + " : Please specify a server name as an argument. Exiting...")
        print(Fore.RESET + Back.RESET + Style.RESET_ALL)
        exit()
