from pony.orm import *
from datetime import datetime

db = Database()


class DeliveryType(db.Entity):
    type_name = PrimaryKey(str)
    delivery = Optional('Delivery')


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
    order = Set('OrderInfo')


class Order(db.Entity):
    number = Required('OrderInfo')
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
    order = Set(Order)


class OrderInfo(db.Entity):
    number = PrimaryKey(int, auto=True)
    client = Required(Client)
    order = Set(Order)


db.bind('sqlite', 'chef.db', create_db=True)
db.generate_mapping(create_tables=True)