import os
import requests
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
    photo1 = Photos(local_path='static/images/deliveries/tashir.png')
    photo2 = Photos(local_path='static/images/deliveries/2berega.jpg')
    photo3 = Photos(local_path='static/images/deliveries/sushiWOK.jpg')
    photo4 = Photos(local_path='static/images/deliveries/rokenrolli.jpg')
    photo5 = Photos(local_path='static/images/deliveries/brash.jpg')
    photo6 = Photos(local_path='static/images/deliveries/tamada.jpg')
    pizza1 = Photos(local_path='static/images/menu/pizza1.jpg')
    pizza2 = Photos(local_path='static/images/menu/pizza2.jpg')
    dt1 = DeliveryType(type_name='🍕 Пиццерии')
    dt2 = DeliveryType(type_name='🍣 Суши')
    dt3 = DeliveryType(type_name='🍖 На углях')
    d1 = Delivery(name='Ташир', type=dt1, cook_chat_username='basbk', photo=photo1)
    d2 = Delivery(name='2 Берега', type=dt1, cook_chat_username='774123748', photo=photo2)
    d3 = Delivery(name='Суши WOK', type=dt2, cook_chat_username='124123748', photo=photo3)
    d4 = Delivery(name='Рокенроллы', type=dt2, cook_chat_username='654423948', photo=photo4)
    d5 = Delivery(name='Браш', type=dt3, cook_chat_username='654123118', photo=photo5)
    d6 = Delivery(name='Тамада', type=dt3, cook_chat_username='654123998', photo=photo6)
    Couriers(username='basbk', delivery=d1)
    Menu(delivery_name=d1, name='4 сыра', description='сыр Брынза, сыр Фетакса, сыр Моцарелла, сыр Пармезан', weight=1500, price=650, photo=pizza1)
    Menu(delivery_name=d1, name='Мясная', description='мясной фарш, сыр Моцарелла, аджика, соус Томатный, соус "Маджорио", укроп', weight=1600, price=750, photo=pizza2)
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
    return 'success'


@app.route('/api/dropit')
def drop_the_base():
    db.drop_all_tables(with_all_data=True)
    return 'done'


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
    if types == []:
        return 'There is no delivery types', 404
    return jsonify(types), 200


@app.route('/api/deliveries/<string:dtype>')
@db_session
def deliveries_by_type(dtype):
    if DeliveryType.exists(type_name=dtype):
        result = []
        for d in Delivery.select(lambda deliv: deliv.type.type_name == dtype):
            result.append(d.to_dict())
        if result == []:
            return 'There are no deliveries with such type', 404
        return jsonify(result), 200
    return 'Such delivery type doesnt exists', 404


@app.route('/api/clients')
@db_session
def clients():
    clients = []
    for c in Client.select():
        clients.append(c.to_dict())
    if clients == []:
        return 'There are no clients', 200
    return jsonify(clients)


@app.route('/api/menu')
@db_session
def menu():
    menu = []
    for m in Menu.select():
        menu.append(m.to_dict())
    if menu == []:
        return 'There is no menus', 200
    return jsonify(menu)


@app.route('/api/deliveries', methods=['POST'])
@db_session
def add_delivery():
    req = request.get_json()
    if req is not None:
        try:
            delivery = Delivery(name=req['name'], type=DeliveryType.get(type_name=req['type_name']),
                                courier_chatID=req['courier_chatID'], cook_chatID=req['cook_chatID'])
            return jsonify(delivery.to_dict())
        except TypeError:
            return 'Bad JSON', 400
    return 'Bad or corrupt JSON', 400


@app.route('/api/clients', methods=['POST'])
@db_session
def new_client():
    req = json.loads(request.get_json())
    if req is not None:
        try:
            client = Client.get(username=req['username'])
            if client is None:
                address = Address(latitude=req['latitude'], longitude=req['longitude'], additional_info=req['additional_info'])
                client = Client(username=req['username'], address=address)
            else:
                client.address.set(latitude=req['latitude'], longitude=req['longitude'], additional_info=req['additional_info'])
            return jsonify(client.to_dict())
        except TypeError:
            return 'Bad JSON', 400
    return 'Bad or corrupt JSON', 400


@app.route('/api/orders/<string:username>', methods=['POST'])
@db_session
def place_order(username):
    if Client.exists(username=username):
        order = Order(client=Client[username])
        menu = []
        for i in ShoppingCart.select(lambda cart: cart.username == username):
            menu.append({'name': i.menu_position.name, 'count': i.count})
            o = OrderInfo(number=order, date=datetime.now(), menu_position=i.menu_position, count=i.count)
        if menu == []:
            return 'The cart is empty', 404
        ShoppingCart.select(lambda cart: cart.username == username).delete(bulk=True)
        return jsonify({'order_number': order.number,
                        'cook': o.menu_position.delivery_name.cook_chat_id,
                        'menu': menu})
    return 'There is no such client', 404


@app.route('/api/orders/<int:number>', methods=['PUT'])
@db_session
def update_order(number):
    if Order.exists(number=number):
        order = Order[number]
        menu = []
        order.status = 1
        courier = OrderInfo.select(lambda o: o.number.number == number).first().menu_position.delivery_name.couriers_chat_username.select(lambda c: c.busy is False).first()
        if courier is not None:
            order.courier = courier
            courier.busy = True
            for i in order.info:
                menu.append({'name': i.menu_position.name, 'count': i.count})
            location = get_location(order.client.address.additional_info)
            return jsonify({'order_number': number,
                            'client': order.client.username,
                            'courier': courier.chat_id,
                            'menu': menu,
                            'address': {'text': order.client.address.additional_info,
                                        'lat': location.split(' ')[1],
                                        'long': location.split(' ')[0]}})
        return 'All couriers are busy', 404
    return 'There is no such order', 404


@app.route('/api/orders/courier/<string:username>', methods=['PUT'])
@db_session
def finish_order(username):
    if Couriers.exists(username=username):
        try:
            Order.get(lambda o: o.courier.username == username and o.status == 1).status = 2
        except Exception:
            return 'There is no order for that courier', 404
        Couriers[username].busy = False
        return '', 200
    return 'There is no such courier', 404


def get_location(info):
    url = 'https://geocode-maps.yandex.ru/1.x/?geocode={0}&format=json&kind=house&results=1'
    address = 'Ростов-на-Дону,+' + info.replace(' ', '+')
    r = requests.get(url.format(address))
    return r.json()['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']


@app.route('/api/staff/<string:username>', methods=['PUT'])
@db_session
def set_chat_id_for_staff(username):
    req = json.loads(request.get_json())
    if req is not None:
        cook = Delivery.get(cook_chat_username=username)
        courier = Couriers.get(username=username)
        if cook is not None:
            cook.cook_chat_id = req['chatID']
        if courier is not None:
            courier.chat_id = req['chatID']
            return '', 200
        else:
            return 'There is no such employee', 404
    return 'Bad or corrupt JSON', 400


@app.route('/api/cart/<string:client>', methods=['GET', 'POST', 'DELETE'])
@db_session
def manage_cart(client):
    if request.method == 'GET':
        result = []
        i = 0
        for c in ShoppingCart.select(lambda cart: cart.username == client):
            result.append(c.to_dict())
            result[i]['price'] = Menu[result[i]['menu_position']].price
            result[i]['menu_position'] = Menu[result[i]['menu_position']].name
            i += 1
        if result == []:
            return 'Cart is empty', 404
        return jsonify(result)
    elif request.method == 'POST':
        req = json.loads(request.get_json())
        if req is not None:
            cart = ShoppingCart.get(username=client,
                                    menu_position=Menu.get(delivery_name=Delivery.get(name=req['delivery']), name=req['menu_name']))
            if cart is None:
                cart = ShoppingCart(username=client,
                                    menu_position=Menu.get(delivery_name=Delivery.get(name=req['delivery']), name=req['menu_name']),
                                    count=1, date=datetime.now())
            else:
                cart.count += 1
            return jsonify({'count': cart.count})
        return 'Bad or corrupt JSON', 400
    else:
        req = json.loads(request.get_json())
        if req is not None:
            if req['whole']:
                ShoppingCart.select(lambda cart: cart.username == client).delete(bulk=True)
                return '', 200
            else:
                ShoppingCart.get(username=client, menu_position=req['menu_position']).delete()
                return '', 200
        return 'Bad or corrupt JSON', 400


@app.route('/api/menu/<string:delivery>')
@db_session
def menu_by_delivery(delivery):
    if Delivery.exists(name=delivery):
        result = []
        for m in Menu.select(lambda menu: menu.delivery_name.name == delivery):
            result.append(m.to_dict())
        if result == []:
            return 'There is no menu for this delivery', 404
        return jsonify(result)
    return 'Such delivery doesnt exists', 404


@app.route('/api/menu', methods=['POST'])
@db_session
def add_menu_item():
    req = request.get_json()
    if req is not None:
        try:
            menu = Menu(delivery_name=req['delivery_name'], name=req['name'], description=req['description'],
                        weight=req['weight'], price=req['price'], photo=req['photo'])
        except TypeError:
            return 'Bad JSON', 400
        return jsonify(menu.to_dict())
    return 'Bad or corrupt JSON', 400


@app.route('/api/menu/<string:m_name>/photo', methods=['PUT'])
@db_session
def set_menu_photo_id(m_name):
    m = Menu.get(name=m_name)
    if m is not None:
        if request.args is not None:
            m.photo_id = request.args.get('photo_id')
            return m
        return 'There is no arguments', 400
    return 'There is no such menu item', 404


@app.route('/api/deliveries/<string:d_name>/photo', methods=['PUT'])
@db_session
def set_delivery_photo_id(d_name):
    d = Delivery[d_name]
    if d is not None:
        if request.args is not None:
            d.photo_id = request.args.get('photo_id')
            return d
        return 'There is no arguments', 400
    return 'There is no such delivery', 404


if __name__ == '__main__':
    app.config['JSON_AS_ASCII'] = False
    # app.run(host="192.168.1.235", port=os.environ.get('PORT', 5000))
    # app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
    app.run(debug=True)
