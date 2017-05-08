from pony.orm import *
from datetime import datetime

db = Database()


class DeliveryType(db.Entity):
    type_name = PrimaryKey(str)
    delivery = Set('Delivery')


class Delivery(db.Entity):
    name = PrimaryKey(str)
    type = Required(DeliveryType)
    courier_chatID = Required(int)
    cook_chatID = Required(int)
    photo = Optional('Photos')
    photo_id = Optional(str)
    menu = Set('Menu', cascade_delete=True)


class Address(db.Entity):
    latitude = Optional(float)
    longitude = Optional(float)
    additional_info = Required(str)
    client = Optional('Client')


class Client(db.Entity):
    username = PrimaryKey(str)
    address = Required(Address, cascade_delete=True)
    order = Set('Order', cascade_delete=True)


class OrderInfo(db.Entity):
    number = Required('Order')
    date = Required(datetime)
    menu_position = Required('Menu')
    count = Required(int)


class Menu(db.Entity):
    delivery_name = Required(Delivery)
    name = Required(str)
    description = Required(str)
    weight = Required(float)
    price = Required(float)
    photo = Optional('Photos')
    photo_id = Optional(str)
    order = Set(OrderInfo, cascade_delete=True)
    cart = Set('ShoppingCart', cascade_delete=True)


class Order(db.Entity):
    number = PrimaryKey(int, auto=True)
    client = Required(Client)
    info = Set(OrderInfo, cascade_delete=True)


class ShoppingCart(db.Entity):
    username = Required(str)
    menu_position = Required(Menu)
    count = Required(int)
    date = Required(datetime)


class Photos(db.Entity):
    local_path = PrimaryKey(str)
    delivery = Optional(Delivery)
    menu = Optional(Menu)


db.bind('postgres', dbname="ChefDB", user="postgres",
        password="2001977s",
        host='localhost', port='5432')
# db.bind('postgres', dbname="d3atsp68tiv44j", user="wuwecbvljbvmpe",
#         password="5e04751395ea098f11e4b89c63acf6ae1e8155f97a39919659541d3368029334",
#         host='ec2-176-34-111-152.eu-west-1.compute.amazonaws.com', port='5432')
db.generate_mapping(create_tables=True)
