from flask import Flask, jsonify
from pony.orm.serialization import to_dict, to_json
from models import *
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def helloworld():
    return 'Hello world!'


@app.route('/api/populate')
@db_session
def populate():
    dt1 = DeliveryType(type_name='Пиццерия')
    d1 = Delivery(name='Ташир', type=dt1, courier_chatID='@courier', cook_chatID='@cooking')
    m1 = Menu(delivery_name=d1, name='4 сыра', description='Вкуснота', weight=1500, price=650)
    m2 = Menu(delivery_name=d1, name='Мясная', description='Ваще оч вкусно', weight=1600, price=750)
    a1 = Address(latitude=58.264846, longitude=65.211548, additional_info='подъезд 2, кв. 348, этаж 16')
    c1 = Client(chatID='@client', address=a1)
    oi1 = OrderInfo(client=c1)
    Order(number=oi1, date=datetime.now(), menu_position=m1, count=2)
    Order(number=oi1, date=datetime.now(), menu_position=m2, count=1)
    oi2 = OrderInfo(client=c1)
    Order(number=oi2, date=datetime.now(), menu_position=m2, count=3)
    return 'success'


@app.route('/api/orders')
@db_session
def orders():
    orders = []
    for o in OrderInfo.select():
        orders.append(o.to_dict(with_collections=True))
    return jsonify(orders)


@app.route('/api/orders_info')
@db_session
def orders_info():
    orders = []
    for o in Order.select():
        orders.append(o.to_dict(with_collections=True))
    return jsonify(orders)


@app.route('/api/orders/<int:number>')
def orders_by_num(number):
    return jsonify(model_to_dict(Order.select().where(Order.number == number).get(), recurse=False))


if __name__ == '__main__':
    # app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    app.run(debug=True)