from flask import Flask, jsonify
from playhouse.shortcuts import *
from models import *
from datetime import date

app = Flask(__name__)


@app.route('/')
def helloworld():
    return 'Hello world!'


@app.route('/api/populate')
def populate():
    db.create_tables([DeliveryType, Delivery, Menu, Address, Client, Order, OrderMenuThrough], safe=True)
    dt1 = DeliveryType.create(type_name='Пиццерия')
    d1 = Delivery.create(name='Ташир', type=dt1, courier_chatID='@courier', cook_chatID='@cooking')
    m1 = Menu.create(delivery_name=d1, name='4 сыра', description='Вкуснота', weight=1500, price=650)
    m2 = Menu.create(delivery_name=d1, name='Мясная', description='Ваще оч вкусно', weight=1600, price=750)
    a1 = Address.create(latitude=58.264846, longitude=65.211548, additional_info='подъезд 2, кв. 348, этаж 16')
    c1 = Client.create(chatID='@client', address=a1)
    o1 = Order.create(date=date.today(), count=2, client=c1)
    o2 = Order.create(date=date.today(), count=3, client=c1)
    o1.menu_position.add(o1)
    return 'success'


@app.route('/api/orders')
def orders():
    orders = []
    [orders.append(model_to_dict(o, recurse=False)) for o in Order.select()]
    return jsonify(orders)



@app.route('/api/orders/<int:number>')
def orders_by_num(number):
    return jsonify(model_to_dict(Order.select().where(Order.number == number).get(), recurse=False))


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    app.run(debug=True)