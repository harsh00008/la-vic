__author__ = 'Harsh Malewar'

class Order():

    def __init__(self, message_type, token_number, order_details, cost, tax, total):
        self.message_type = message_type
        self.token_number = token_number
        self.order_details = order_details
        self.cost = cost
        self.total = total

    def print_order_details(self):
        print("Token Number: " + str(self.token_number))

    def get_token_number(self):
        return self.token_number

    def set_message_type(self, message_type):
        self.message_type = message_type

class Item():

    def __init__(self, item_name, unit_cost, quantity):
        self.item_name = item_name
        self.unit_cost = unit_cost
        self.quantity = quantity

    def print_item_details(self):
        print("Item Name: " + self.item_name)
        print("Unit Cost: " + self.unit_cost)
        print("Quantity: " + self.quantity)
