from pony.orm import *
from datetime import datetime

db = Database()


class DeliveryType(db.Entity):
    type_name = PrimaryKey(str)
    delivery = Set('Delivery')


class Delivery(db.Entity):
    name = PrimaryKey(str)
    type = Required(DeliveryType)
    courier_chatID = Required(str)
    cook_chatID = Required(str)
    menu = Set('Menu')


class Address(db.Entity):
    latitude = Required(float)
    longitude = Required(float)
    additional_info = Required(str)
    client = Optional('Client')


class Client(db.Entity):
    chatID = PrimaryKey(str)
    address = Required(Address)
    order = Set('Order')


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
    photo = Optional(str)
    photo_id = Optional(str)
    order = Set(OrderInfo)


class Order(db.Entity):
    number = PrimaryKey(int, auto=True)
    client = Required(Client)
    info = Set(OrderInfo)


db.bind('postgres', dbname="d3atsp68tiv44j", user="wuwecbvljbvmpe",
        password="5e04751395ea098f11e4b89c63acf6ae1e8155f97a39919659541d3368029334",
        host='ec2-176-34-111-152.eu-west-1.compute.amazonaws.com', port='5432')
db.generate_mapping(create_tables=True)