import os
from flask import Flask, jsonify, request
from models import *
from datetime import datetime

app = Flask(__name__)


@app.route('/')
def helloworld():
    return 'Lets roll!'


@app.route('/api/populate')
@db_session
def populate():
    dt1 = DeliveryType(type_name='Пиццерия')
    d1 = Delivery(name='Ташир', type=dt1, courier_chatID='@courier', cook_chatID='@cooking')
    m1 = Menu(delivery_name=d1, name='4 сыра', description='Вкуснота', weight=1500, price=650)
    m2 = Menu(delivery_name=d1, name='Мясная', description='Ваще оч вкусно', weight=1600, price=750)
    a1 = Address(latitude=58.264846, longitude=65.211548, additional_info='подъезд 2, кв. 348, этаж 16')
    c1 = Client(chatID='@client', address=a1)
    o1 = Order(client=c1)
    OrderInfo(number=o1, date=datetime.now(), menu_position=m1, count=2)
    OrderInfo(number=o1, date=datetime.now(), menu_position=m2, count=1)
    o2 = Order(client=c1)
    OrderInfo(number=o2, date=datetime.now(), menu_position=m2, count=3)
    return 'success'


@app.route('/api/orders')
@db_session
def orders():
    orders = []
    for o in Order.select():
        orders.append(o.to_dict(with_collections=True))
    return jsonify(orders)


@app.route('/api/orders_info')
@db_session
def orders_info():
    orders_info = []
    for o in OrderInfo.select():
        orders_info.append(o.to_dict(with_collections=True))
    return jsonify(orders_info)


@app.route('/api/deliveries')
@db_session
def deliveries():
    deliveries = []
    for d in Delivery.select():
        deliveries.append(d.to_dict())
    return jsonify(deliveries)


@app.route('/api/delivery_types')
@db_session
def types():
    types = []
    for t in DeliveryType.select():
        types.append(t.to_dict())
    return jsonify(types)


@app.route('/api/deliveries/<string:dtype>')
@db_session
def deliveries_by_type(dtype):
    result = []
    for d in Delivery.select(lambda deliv: deliv.type.type_name == dtype):
        result.append(d.to_dict())
    return jsonify(result)


@app.route('/api/clients')
@db_session
def clients():
    clients = []
    for c in Client.select():
        clients.append(c.to_dict())
    return jsonify(clients)


@app.route('/api/menu')
@db_session
def menu():
    menu = []
    for m in Menu.select():
        menu.append(m.to_dict())
    return jsonify(menu)


@app.route('/api/deliveries', methods=['POST'])
@db_session
def add_delivery():
    req = request.get_json()
    delivery = Delivery(name=req['name'], type=DeliveryType.get(type_name=req['type_name']),
                        courier_chatID=req['courier_chatID'], cook_chatID=req['cook_chatID'])
    return jsonify(delivery.to_dict())


@app.route('/api/clients', methods=['POST'])
@db_session
def new_client():
    req = request.get_json()
    address = Address(latitude=req['latitude'], longitude=req['longitude'], additional_info=req['additional_info'])
    client = Client(chatID=req['chatID'], address=address)
    return jsonify(client.to_dict())


@app.route('/api/orders', methods=['POST'])
@db_session
def place_order():
    req = request.get_json()
    order = Order(client=req['client'])
    for i in req['info']:
        OrderInfo(number=order, date=datetime.now(), menu_position=i['menu_position'], count=i['count'])
    return jsonify(order.to_dict())


@app.route('/api/basket/<string:client>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@db_session
def manage_basket(client):
    req = request.get_json()
    if request.method == 'GET':
        result = []
        for b in Basket.select(lambda basket: basket.client.chatID == client):
            result.append(b.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        basket = Basket(client=client, menu_position=req['menu_position'],
                        count=req['count'], date=datetime.now())
        return jsonify(basket.to_dict())
    elif request.method == 'PUT':
        basket = Basket.get(client=client, menu_position=req['menu_position'])
        basket.count = req['count']
        return jsonify(basket.to_dict())
    else:
        if req['whole']:
            for b in Basket.select(lambda basket: basket.client.chatID == client):
                b.delete()
            return 200
        else:
            Basket.get(client=client, menu_position=req['menu_position']).delete()
            return 200

@app.route('/api/menu/<string:delivery>')
@db_session
def menu_by_delivery(delivery):
    result = []
    for m in Menu.select(lambda menu: menu.delivery_name.name == delivery):
        result.append(m.to_dict())
    return jsonify(result)


@app.route('/api/menu', methods=['POST'])
@db_session
def add_menu_item():
    req = request.get_json()
    menu = Menu(delivery_name=req['delivery_name'], name=req['name'], description=req['description'],
                weight=req['weight'], price=req['price'], photo=req['photo'])
    return jsonify(menu.to_dict())


@app.route('/api/menu/<string:m_name>/photo', methods=['PUT'])
@db_session
def set_menu_photo_id(m_name):
    m = Menu.get(name=m_name)
    m.photo_id = request.args.get('photo_id')
    return m


@app.route('/api/deliveries/<string:d_name>/photo', methods=['PUT'])
@db_session
def set_delivery_photo_id(d_name):
    d = Delivery.get(name=d_name)
    d.photo_id = request.args.get('photo_id')
    return d

if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    # app.run(debug=True)
