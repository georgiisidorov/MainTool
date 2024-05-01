import datetime
import operator
from utils.db_api.db_gino import db
from utils.db_api.schemas.user import User
from utils.db_api.schemas.order import Order
from utils.db_api.schemas.settings import Settings
from utils.db_api.schemas.auto import Auto
from asyncpg import UniqueViolationError


async def add_user(user_id: int, username: str, fullname: str, datetime, test_3k):
    try:
        user = User(user_id=user_id, username=username, fullname=fullname, created_at=datetime, updated_at=datetime, test_3k=test_3k, balance=0)
        await user.create()
    except UniqueViolationError:  
        pass


def sorted_orders(orders, col):
    dict_orders = {}
    for order in orders:
        if col == 'created_at':
            dict_orders[f'{order.order_id}'] = order.created_at
        if col == 'updated_at':
            dict_orders[f'{order.order_id}'] = order.updated_at
    sorted_tuples = sorted(dict_orders.items(), key=operator.itemgetter(1))
    sorted_orders = [k for k, v in sorted_tuples]
    return sorted_orders

def sorted_users(users, col):
    dict_users = {}
    for user in users:
        if col == 'updated_at':
            dict_users[f'{user.user_id}'] = user.updated_at
    sorted_tuples = sorted(dict_users.items(), key=operator.itemgetter(1))
    sorted_users = [k for k, v in sorted_tuples]
    return sorted_users


async def select_user(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def decrease_test_3k(user_id, previous_test_3k, amount):
    user = await User.get(user_id)
    await user.update(test_3k=previous_test_3k-amount).apply()


async def increase_user_balance(user_id, previous_balance, amount):
    user = await User.get(user_id)
    await user.update(balance=previous_balance+amount).apply()


async def decrease_user_balance(user_id, previous_balance, amount):
    user = await User.get(user_id)
    await user.update(balance=previous_balance-amount).apply()


async def updated_at_user(user_id, datetime):
    user = await User.get(user_id)
    await user.update(updated_at=datetime).apply()


async def add_order(order_id: str, user_id: int, action: str, amount: int, service_id: str, description: str, money: float, created_at, status: str = None):
    order = Order(order_id=order_id, user_id=user_id, action=action, amount=amount, service_id=service_id, description=description, status=status, money=money, created_at=created_at)
    await order.create()


async def select_orders_by_user(user_id):
    orders = await Order.query.where(Order.user_id == user_id).gino.all()
    return orders


async def select_order_by_order_id(order_id):
    order = await Order.query.where(Order.order_id == order_id).gino.first()
    return order

 
async def update_order_status(order_id, status):
    order = await Order.query.where(Order.order_id == order_id).gino.first()
    await order.update(status=status).apply()


async def add_settings(id: int, action: str, service_id: str):
    try:
        settings = Settings(id=id, action=action, service_id=service_id)
        await settings.create()
    except UniqueViolationError:  
        pass


async def select_settings(action):
    settings = await Settings.query.where(Settings.action == action).gino.first()
    return settings


async def update_settings(action, service_id):
    settings = await Settings.query.where(Settings.action == action).gino.first()
    await settings.update(service_id=service_id).apply()


async def users_ids_all():
    users_ids = await User.select('user_id').gino.all()
    ids = [id[0] for id in users_ids]
    return ids


async def view_all_users():
    users = await User.query.gino.all()
    return users


async def add_auto(id:int, username: str, user_id: int, service: str, amount: int):
    try:
        auto = Auto(id=id, username=username, service=service, user_id=user_id, amount=amount)
        await auto.create()
    except UniqueViolationError:  
        pass


async def delete_auto_id(id):
    await Auto.delete.where(Auto.id == id).gino.status()


async def select_auto_username(username):
    auto = await Auto.query.where(Auto.username == username).gino.all()
    return auto


async def select_auto_user_id(user_id):
    auto = await Auto.query.where(Auto.user_id == user_id).gino.all()
    return auto