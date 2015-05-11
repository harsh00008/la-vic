__author__ = 'Harsh Malewar'

class Order():

    def __init__(self, token_number, customer_name, order_details):
        self.token_number = token_number
        self.customer_name = customer_name
        self.order_details = order_details

    def print_order_details(self):
        print("Token Number: " + str(self.token_number))

    def get_token_number(self):
        return self.token_number

class Item():

    def __init__(self, item_id, item_name, unit_cost, quantity):
        self.item_id = item_id
        self.item_name = item_name
        self.unit_cost = unit_cost
        self.quantity = quantity

    def print_item_details(self):
        print("Item ID: " + str(self.item_id))
        print("Item Name: " + self.item_name)
        print("Unit Cost: " + self.unit_cost)
        print("Quantity: " + self.quantity)
