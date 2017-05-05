import os
import base64
from flask import Flask, jsonify, request, make_response
from models import *
from datetime import datetime
import json

app = Flask(__name__)


@app.route('/')
def helloworld():
    return 'Lets roll!'


@app.route('/api/populate')
@db_session
def populate():
    with open('images\deliveries\\tashir.jpg', 'rb') as img:
        photo1 = str(base64.b64encode(img.read()))
    with open('images\deliveries\2berega.jpg', 'rb') as img:
        photo2 = str(base64.b64encode(img.read()))
    with open('images\deliveries\sushiWOK.jpg', 'rb') as img:
        photo3 = str(base64.b64encode(img.read()))
    with open('images\deliveries\\rokenrolli.jpg', 'rb') as img:
        photo4 = str(base64.b64encode(img.read()))
    with open('images\deliveries\\brash.jpg', 'rb') as img:
        photo5 = str(base64.b64encode(img.read()))
    with open('images\deliveries\\tamada.jpg', 'rb') as img:
        photo6 = str(base64.b64encode(img.read()))

    dt1 = DeliveryType(type_name='Пиццерии')
    dt2 = DeliveryType(type_name='Суши')
    dt3 = DeliveryType(type_name='На углях')
    d1 = Delivery(name='Ташир', type=dt1, courier_chatID=321546879, cook_chatID=654123748, photo=photo1)
    d2 = Delivery(name='2 Берега', type=dt1, courier_chatID=771546879, cook_chatID=774123748, photo=photo2)
    d3 = Delivery(name='Суши WOK', type=dt2, courier_chatID=881546879, cook_chatID=124123748, photo=photo3)
    d4 = Delivery(name='Рокенроллы', type=dt2, courier_chatID=321545579, cook_chatID=654423948, photo=photo4)
    d5 = Delivery(name='Браш', type=dt3, courier_chatID=321541179, cook_chatID=654123118, photo=photo5)
    d6 = Delivery(name='Тамада', type=dt3, courier_chatID=321599879, cook_chatID=654123998, photo=photo6)
    Menu(delivery_name=d1, name='4 сыра', description='Вкуснота', weight=1500, price=650)
    Menu(delivery_name=d1, name='Мясная', description='Ваще оч вкусно', weight=1600, price=750)
    Menu(delivery_name=d2, name='Гавайская', description='Вкуснота', weight=1500, price=650)
    Menu(delivery_name=d2, name='Пепперони', description='Ваще оч вкусно', weight=1600, price=750)
    Menu(delivery_name=d3, name='Филадельфия', description='Вкуснота', weight=1500, price=650)
    Menu(delivery_name=d3, name='Сашими', description='Ваще оч вкусно', weight=1600, price=750)
    Menu(delivery_name=d4, name='Ролл Фуджи', description='Вкуснота', weight=1500, price=650)
    Menu(delivery_name=d4, name='Ролл Олимп', description='Ваще оч вкусно', weight=1600, price=750)
    Menu(delivery_name=d5, name='Свинная мякоть', description='Вкуснота', weight=1500, price=650)
    Menu(delivery_name=d5, name='Свинная шея', description='Ваще оч вкусно', weight=1600, price=750)
    Menu(delivery_name=d6, name='Баранина мякоть', description='Вкуснота', weight=1500, price=650)
    Menu(delivery_name=d6, name='Люля-кебаб', description='Ваще оч вкусно', weight=1600, price=750)
    # a1 = Address(latitude=58.264846, longitude=65.211548, additional_info='подъезд 2, кв. 348, этаж 16')
    # c1 = Client(chatID=123456789, address=a1)
    # o1 = Order(client=c1)
    # OrderInfo(number=o1, date=datetime.now(), menu_position=m1, count=2)
    # OrderInfo(number=o1, date=datetime.now(), menu_position=m2, count=1)
    # o2 = Order(client=c1)
    # OrderInfo(number=o2, date=datetime.now(), menu_position=m2, count=3)
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


@app.route('/api/cart/<int:client>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@db_session
def manage_cart(client):
    if request.method == 'GET':
        result = []
        for c in ShoppingCart.select(lambda cart: cart.chatID == client):
            result.append(c.to_dict())
        return jsonify(result)
    elif request.method == 'POST':
        req = json.loads(request.get_json())
        cart = ShoppingCart.get(chatID=client,
                                menu_position=Menu.get(delivery_name=Delivery.get(name=req['delivery']), name=req['menu_name']))
        if cart is None:
            cart = ShoppingCart(chatID=client,
                                menu_position=Menu.get(delivery_name=Delivery.get(name=req['delivery']), name=req['menu_name']),
                                count=req['count'], date=datetime.now())
        else:
            cart.count += 1
        return jsonify(cart.to_dict())
    elif request.method == 'PUT':
        req = json.loads(request.get_json())
        cart = ShoppingCart.get(chatID=client,
                                menu_position=Menu.get(delivery_name=Delivery.get(name=req['delivery']), name=req['menu_name']))
        cart.count = req['count']
        return jsonify(cart.to_dict())
    else:
        req = json.loads(request.get_json())
        if req['whole']:
            for c in ShoppingCart.select(lambda cart: cart.chatID == client):
                c.delete()
            return make_response(200)
        else:
            ShoppingCart.get(chatID=client, menu_position=req['menu_position']).delete()
            return make_response(200)


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
