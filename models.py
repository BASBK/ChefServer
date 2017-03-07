from peewee import *
from playhouse.fields import *

db = SqliteDatabase('chef_db.sqlite')


class BaseModel(Model):
    class Meta:
        database = db


class DeliveryType(BaseModel):
    type_name = CharField(primary_key=True)


class Delivery(BaseModel):
    name = CharField(primary_key=True)
    type = ForeignKeyField(DeliveryType, related_name='delivery')
    courier_chatID = CharField()
    cook_chatID = CharField()


class Address(BaseModel):
    latitude = DoubleField()
    longitude = DoubleField()
    additional_info = TextField()


class Client(BaseModel):
    chatID = CharField(primary_key=True)
    address = ForeignKeyField(Address, related_name='client')


class Order(BaseModel):
    number = IntegerField(primary_key=True)
    date = DateTimeField
    #menu_position = ManyToManyField(Menu, related_name='order')
    count = IntegerField()
    client = ForeignKeyField(Client, related_name='order')


class Menu(BaseModel):
    delivery_name = ForeignKeyField(Delivery, related_name='menu')
    name = CharField()
    description = TextField()
    weight = DoubleField()
    price = DoubleField()
    photo = CharField(default='none')
    order = ManyToManyField(Order, related_name='menu_position')


OrderMenuThrough = Menu.order.get_through_model()