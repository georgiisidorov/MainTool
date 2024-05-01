import datetime
import logging
import random

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message, CallbackQuery, ContentType, MediaGroup, InlineKeyboardButton, InlineKeyboardMarkup, LabeledPrice, PreCheckoutQuery
from aiogram.types.input_media import InputMediaPhoto
from aiogram.utils.exceptions import BotBlocked, ChatNotFound
import asyncio

from data import config
from handlers.users.jap_api import api_service, api_status
from keyboards.inline.button import main_keyboard, main_keyboard_test, balance_keyboard, services_keyboard, markup_pay, prices_keyboard, reactions_keyboard, return_keyboard, main_keyboard_VIP, main_keyboard_VIP_test, commands_keyboard, confirm_keyboard, statistics_keyboard, commands_return_keyboard, services_keyboard_instant, auto_keyboard, cancel_keyboard, auto_buttons_keyboard, markup_disconnect
from loader import dp
from states.states import States
from utils.db_api import quick_commands
from utils.misc.qiwi import Payment, NoPaymentFound, NotEnoughMoney


rct = {"6571": "👍", "6572": "👎", "6573": "❤️", "6574": "🔥", "6575": "🎉", 
    "6576": "🤩", "6577": "😱", "6578": "😁", "6579": "😢", "6580": "💩", 
    "6581": "🤮"}

def time_now():
    now = str(datetime.datetime.now())
    index_dot = now.index('.')
    now = now[:index_dot] + ' по МСК'
    return now


# Просим ввести количество подписчиков
@dp.message_handler(CommandStart())
async def start(message: Message, state: FSMContext):
    user_id = message.from_user.id

    try:
        fullname = message.from_user.first_name + ' ' + message.from_user.last_name
    except TypeError:
        fullname = message.from_user.first_name

    username = message.from_user.username or None
    await quick_commands.add_user(user_id, username, fullname, datetime.datetime.now(), 3000)

    user = await quick_commands.select_user(user_id)
    if message.from_user.id in [1247122892, 1048524289, 83335761]:
        if user.test_3k > 0:
            msg = await message.answer('Этот бот увеличивает количество подписчиков и просмотров на постах в телеграм-пабликах', reply_markup=main_keyboard_VIP_test)
            await state.update_data(message_id=msg.message_id)
        else:
            msg = await message.answer('Этот бот увеличивает количество подписчиков и просмотров на постах в телеграм-пабликах', reply_markup=main_keyboard_VIP)
            await state.update_data(message_id=msg.message_id)
    else:
        if user.test_3k > 0:
            msg = await message.answer('Этот бот увеличивает количество подписчиков и просмотров на постах в телеграм-пабликах', reply_markup=main_keyboard_test)
            await state.update_data(message_id=msg.message_id)
        else:
            msg = await message.answer('Этот бот увеличивает количество подписчиков и просмотров на постах в телеграм-пабликах', reply_markup=main_keyboard)
            await state.update_data(message_id=msg.message_id)


# @dp.message_handler()
# async def frhefh(message: Message):
#     if message.from_user.id == 1247122892:
#         await message.answer(message)


# @dp.message_handler(content_types=ContentType.DOCUMENT)
# async def frhefh(message: Message):
#     if message.from_user.id == 1247122892:
#         await message.answer(message)


# @dp.message_handler(content_types=ContentType.ANY)
# async def frhefh(message: Message):
#     if message.from_user.id == 1247122892:
#         await message.answer(message)


# @dp.message_handler(content_types=ContentType.AUDIO)
# async def frhefh(message: Message):
#     if message.from_user.id == 1247122892:
#         await message.answer(message)


# ----------------------- Б А Л А Н С ------------------------


@dp.callback_query_handler(text='balance')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Выберите действие с балансом', 
        reply_markup=balance_keyboard)


@dp.callback_query_handler(text='deposit')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text('Введите ту сумму, на которую Вы хотите пополнить кошелёк (в рублях)', reply_markup=return_keyboard)
    await States.Deposit.set()


@dp.callback_query_handler(text='checkbalance')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = await quick_commands.select_user(call.from_user.id)
    await call.message.edit_text(f'Ваш баланс: <b>{round(user.balance, 2)}₽</b>', 
        parse_mode='html', reply_markup=return_keyboard)


@dp.message_handler(state=States.Deposit, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    try:
        amount = int(message.text)
        await message.delete()
        if amount < 100 and amount > 1:
            await dp.bot.edit_message_text("Минимальная сумма пополнения - 100₽", user_id, message_id, reply_markup=return_keyboard)
        else:
            payment = Payment(amount=amount)
            payment.create()

            markup = await markup_pay(payment.invoice)

            await dp.bot.edit_message_text(
                f"Вы собираетесь пополнить кошелёк на <b>{amount}₽</b>", user_id, message_id, 
                parse_mode='html', reply_markup=markup)

            await state.update_data(
                amount=amount,
                id_deposit=payment.id
            )
            await States.Payment.set()

            # await state.finish()
            # await dp.bot.send_invoice(
            #     chat_id=message.from_user.id,
            #     title=f'UpTool Payment',
            #     description=f'Пополнение кошелька на {amount}₽',
            #     payload=str(random.randint(0, 10000000)),
            #     provider_token=config.PROVIDER_TOKEN,
            #     currency='RUB',
            #     start_parameter=f'deposit_{amount}_rub',
            #     prices=[
            #         LabeledPrice(
            #             label=f'Пополнение на {amount}₽',
            #             amount=amount*100
            #         )
            #     ]
            # )
    except ValueError:
        await message.delete()
        await dp.bot.edit_message_text("Неверное значение, введите число", user_id, message_id, reply_markup=return_keyboard)


# @dp.pre_checkout_query_handler()
# async def process_pre_checkout_query(query: PreCheckoutQuery):
#     await dp.bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, 
#         ok=True)
#     user = await quick_commands.select_user(message.from_user.id)
#     previous_balance = user.balance
#     await quick_commands.increase_user_balance(message.from_user.id, previous_balance, amount)
#     await dp.bot.send_message(chat_id=query.from_user.id, 
#         text='Ваш кошелёк пополнен!')





@dp.callback_query_handler(state=States.Payment, text='paid')
async def approve_payment(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    amount = data.get("amount")
    id_deposit = data.get("id_deposit")
    payment = Payment(amount=amount, id=id_deposit)
    markup = await markup_pay(payment.invoice)
    try:
        payment.check_payment()
    except NoPaymentFound:
        await call.message.edit_text("Транзакция не найдена", reply_markup=markup)
        return
    except NotEnoughMoney:
        await call.message.edit_text("Оплаченная сумма меньше необходимой", reply_markup=markup)
        return

    else:
        user = await quick_commands.select_user(call.from_user.id)
        previous_balance = user.balance
        await quick_commands.increase_user_balance(call.from_user.id, previous_balance, amount)
        await quick_commands.updated_at_user(
                call.from_user.id, datetime.datetime.now())
        await call.message.edit_text(f'Ваш баланс пополнен на <b>{amount}₽</b>!', parse_mode='html', reply_markup=return_keyboard)
        await state.finish()
        await state.update_data(message_id=call.message.message_id)



# ----------------------- У С Л У Г И -------------------------


@dp.callback_query_handler(text='order')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = await quick_commands.select_user(call.from_user.id)
    orders = await quick_commands.select_orders_by_user(user.user_id)
    sorted_orders_ids = quick_commands.sorted_orders(orders, 'created_at')
    sorted_orders = []
    if sorted_orders_ids != []:
        for order_id in sorted_orders_ids:
            sorted_orders.append(await quick_commands.select_order_by_order_id(order_id))
        
        services_keyboard_last_order = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Просмотры", callback_data="views"),
            InlineKeyboardButton(text="Подписчики", callback_data="subs"),
            InlineKeyboardButton(text="Реакции", callback_data="reactions")],
            [InlineKeyboardButton(text="Повторить заказ ↩️", callback_data=f"repeat:{sorted_orders[-1].action}:{sorted_orders[-1].amount}:{sorted_orders[-1].service_id}:{sorted_orders[-1].money}")],
            [InlineKeyboardButton(text="Главное меню 📁", callback_data="cancel")]
        ])
    if orders == []:
        await call.message.edit_text('Выберите заказ по продвижению', 
            reply_markup=services_keyboard)
    else:
            if sorted_orders[-1].action == 'reactions':
                await call.message.edit_text(f'Выберите заказ по продвижению\n\nP.S. Вы также можете повторить последний заказ: <b>{sorted_orders[-1].amount} реакций</b> {rct[f"{sorted_orders[-1].service_id}"]}', reply_markup=services_keyboard_last_order)
            elif sorted_orders[-1].action == 'views':
                await call.message.edit_text(f'Выберите заказ по продвижению\n\nP.S. Вы также можете повторить последний заказ: <b>{sorted_orders[-1].amount} просмотров</b>', reply_markup=services_keyboard_last_order)
            elif sorted_orders[-1].action == 'subs':
                await call.message.edit_text(f'Выберите заказ по продвижению\n\nP.S. Вы также можете повторить последний заказ: <b>{sorted_orders[-1].amount} подписчиков</b>', reply_markup=services_keyboard_last_order)


# --------------------- П Р О С М О Т Р Ы ---------------------


@dp.callback_query_handler(text='views')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text('Перешлите в чат тот пост, на который Вы хотите выбранное количество просмотров', reply_markup=return_keyboard)
    await States.Views_Link.set()


@dp.callback_query_handler(text='views_instant')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text('Введите количество просмотров, которые Вы хотите заказать', reply_markup=return_keyboard)
    await States.Views.set()


@dp.message_handler(state=States.Views_Link, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    if message.forward_from_chat.username is None:
        await dp.bot.edit_message_text('Услуги не работают в принципе для частных каналов', user_id, message_id, reply_markup=return_keyboard)
        await message.delete()
    else:
        try:
            link = 'https://t.me/' + message.forward_from_chat.username + '/' + str(message.forward_from_message_id)
            await message.delete()
            await state.update_data(link=link)            
            await dp.bot.edit_message_text('Введите количество просмотров, которые Вы хотите заказать', user_id, message_id, reply_markup=return_keyboard)
            await States.Views.set()
        except AttributeError:
            await message.delete()


@dp.message_handler(state=States.Views, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    try:
        amount = int(message.text)
        await message.delete()
        if amount < 100:
            await dp.bot.edit_message_text("Минимальное количество просмотров - 100", user_id, message_id, reply_markup=return_keyboard)
        else:
            user = await quick_commands.select_user(user_id)
            balance = user.balance
            money = round((amount * 0.003), 2)
            if round(balance, 2) < money:
                await dp.bot.edit_message_text('Недостаточно средств на балансе! Заказ отменён.', user_id, message_id, reply_markup=return_keyboard)
            else:
                link = data.get("link")
                await quick_commands.decrease_user_balance(user_id, balance, money)
                await quick_commands.updated_at_user(
                    user_id, datetime.datetime.now())
                sss = await quick_commands.select_settings('views')
                service_id = sss.service_id
                order = await api_service(service_id, link, amount)
                await quick_commands.add_order(str(order), user_id, 'views', amount, None, f'от {time_now()} на <b>{amount}</b> просмотров на пост {link}', money, datetime.datetime.now())
                await dp.bot.edit_message_text(f'Заказ выполняется! Стоимость - {money}₽', user_id, message_id, reply_markup=return_keyboard)
                await state.finish()
                await state.update_data(message_id=message_id)
            
    except ValueError:
        await message.delete()
        await dp.bot.edit_message_text("Неверное значение, введите число", user_id, message_id, reply_markup=return_keyboard)



# -------------------------- П О Д П И С Ч И К И ----------------------------


@dp.callback_query_handler(text='subs')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text(
        "Перешлите в чат любой пост того канала, на который Вы хотите привлечь подписчиков",
        reply_markup=return_keyboard)
    await States.Subs_Link.set()


@dp.callback_query_handler(text='subs_instant')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text(
        "Введите количество подписчиков, которое хотите привлечь на канал",
        reply_markup=return_keyboard)
    await States.Subs.set()


@dp.message_handler(state=States.Subs_Link, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    if message.forward_from_chat.username is None:
        await dp.bot.edit_message_text('Услуги не работают в принципе для частных каналов', user_id, message_id, reply_markup=return_keyboard)
        await message.delete()
        await state.finish()
    else:
        try:
            link_username = 'https://t.me/' + message.forward_from_chat.username
            await message.delete()
            await state.update_data(link_username=link_username)
            await dp.bot.edit_message_text('Введите количество подписчиков, которое хотите привлечь на канал', user_id, message_id, reply_markup=return_keyboard)
            await States.Subs.set()
        except AttributeError:
            await message.delete()


@dp.message_handler(state=States.Subs, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    try:
        amount = int(message.text)
        await message.delete()
        if amount < 500:
            await dp.bot.edit_message_text("Минимальное количество подписчиков - 500", user_id, message_id, reply_markup=return_keyboard)
        else:
            user = await quick_commands.select_user(user_id)
            balance = user.balance
            money = round((amount * 0.25), 2)
            if round(balance, 2) < money:
                await dp.bot.edit_message_text('Недостаточно средств на балансе! Заказ отменён.', user_id, message_id, reply_markup=return_keyboard)
            else:
                link_username = data.get("link_username")
                await quick_commands.decrease_user_balance(user_id, balance, money)
                await quick_commands.updated_at_user(
                    user_id, datetime.datetime.now())
                sss = await quick_commands.select_settings('subs')
                service_id = sss.service_id
                order = await api_service(service_id, link_username, amount)
                await quick_commands.add_order(str(order), user_id, 'subs', amount, None, f'от {time_now()} на <b>{amount}</b> подписчиков на канал {link_username}', money, datetime.datetime.now())
                await dp.bot.edit_message_text(f'Заказ выполняется! Стоимость - {money}₽. Старт выполнения от 1 до 60 минут.', user_id, message_id, reply_markup=return_keyboard)
                await state.finish()
                await state.update_data(message_id=message_id)
            
    except ValueError:
        await message.delete()
        await dp.bot.edit_message_text("Неверное значение, введите число", user_id, message_id, reply_markup=return_keyboard)



# --------------------------- Р Е А К Ц И И ------------------------------


@dp.callback_query_handler(text='reactions')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text(
        "Перешлите в чат тот пост, на который Вы хотите выбранные реакции",
        reply_markup=return_keyboard
    )
    await States.Reactions_Link.set()


@dp.callback_query_handler(text='reactions_instant')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text(
        "Выберите, какую реакцию Вы хотите",
        reply_markup=reactions_keyboard
    )


@dp.message_handler(state=States.Reactions_Link, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    if message.forward_from_message_id is None:
        await message.delete()
    else:
        if message.forward_from_chat.username is None:
            await dp.bot.edit_message_text('Услуги не работают в принципе для частных каналов', user_id, message_id, reply_markup=return_keyboard)
            await message.delete()
        else:
            link = 'https://t.me/' + message.forward_from_chat.username + '/' +str(message.forward_from_message_id)
            await message.delete()
            await state.update_data(link=link)
            await dp.bot.edit_message_text('Выберите, какую реакцию Вы хотите', user_id, message_id, reply_markup=reactions_keyboard)


@dp.callback_query_handler(text_contains='reaction:')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    service_id = call.data.split(':')[-1]
    await state.update_data(service_id=service_id)
    await call.message.edit_text(
        'Введите то число реакций, которые Вы хотите заказать', 
        reply_markup=return_keyboard
    )
    await States.Reactions.set()


@dp.message_handler(state=States.Reactions, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    try:
        amount = int(message.text)
        await message.delete()
        if amount < 50:
            await dp.bot.edit_message_text("Минимальное количество реакций - 50", user_id, message_id, reply_markup=return_keyboard)
        else:
            user = await quick_commands.select_user(message.from_user.id)
            balance = user.balance
            money = round((amount * 0.2), 2)
            if round(balance, 2) < money:
                await dp.bot.edit_message_text('Недостаточно средств на балансе! Заказ отменён.', user_id, message_id, reply_markup=return_keyboard)
            else:
                service_id = data.get("service_id")
                link = data.get("link")
                await quick_commands.decrease_user_balance(user_id, balance, money)
                await quick_commands.updated_at_user(
                    user_id, datetime.datetime.now())
                order = await api_service(service_id, link, amount)
                await quick_commands.add_order(str(order), user_id, 'reactions', amount, service_id, f'от {time_now()} на <b>{reactions_amount}</b> реакций {rct[f"{service_id}"]} на пост {link}', money, datetime.datetime.now())
                await dp.bot.edit_message_text(f'Заказ выполняется! Стоимость - {money}₽. Старт выполнения от 1 до 60 минут.', user_id, message_id, reply_markup=return_keyboard)
                await state.finish()
                await state.update_data(message_id=message_id)
                
            
    except ValueError:
        await message.delete()
        await dp.bot.edit_message_text("Неверное значение, введите число", user_id, message_id, reply_markup=return_keyboard)    


# ------------------- Т Е С Т О В Ы Е   3 К -------------------


@dp.callback_query_handler(text='test_3k')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = await quick_commands.select_user(call.from_user.id)
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text(f'У Вас осталось <b>{user.test_3k}</b> просмотров.\n\nПерешлите в чат тот пост, на который Вы хотите халявные просмотры', reply_markup=return_keyboard)
    await States.Test_3K.set()


@dp.callback_query_handler(text='test_3k_instant')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = await quick_commands.select_user(call.from_user.id)
    await state.update_data(message_id=call.message.message_id)
    await call.edit_message_text(f'У Вас осталось <b>{user.test_3k}</b> просмотров.\n\nВведите количество просмотров, которые Вы хотите заказать', reply_markup=return_keyboard)
    await States.Test_3K_Views.set()   


@dp.message_handler(state=States.Test_3K_Views, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    user = await quick_commands.select_user(user_id)
    try:
        amount = int(message.text)
        await message.delete()
        if amount < 100:
            await dp.bot.edit_message_text("Минимальное количество просмотров - 100", user_id, message_id, reply_markup=return_keyboard)
        elif amount > user.test_3k:
            await dp.bot.edit_message_text(f"Вы ввели количество просмотров, превышающее доступное. У Вас осталось {user.test_3k} халявных просмотров. Можете попробовать ещё раз", user_id, message_id, reply_markup=return_keyboard)
        else:
            link = data.get('link')
            sss = await quick_commands.select_settings('views')
            service_id = sss.service_id
            await quick_commands.decrease_test_3k(user_id, user.test_3k, amount)
            order = await api_service(service_id, link, amount)
            await quick_commands.add_order(str(order), user_id, 'views', amount, None, f'от {time_now()} на <b>{amount}</b> халявных просмотров на пост {link}', 0, datetime.datetime.now())
            await dp.bot.edit_message_text(f'Заказ выполняется!', user_id, message_id, reply_markup=return_keyboard)
            await state.finish() 
            await state.update_data(message_id=message_id) 

    except ValueError:
        await message.delete()
        await dp.bot.edit_message_text("Неверное значение, введите число", user_id, message_id, reply_markup=return_keyboard)


@dp.message_handler(state=States.Test_3K, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    if message.forward_from_message_id is None:
        await message.delete()
    else:
        if message.forward_from_chat.username is None:
            await dp.bot.edit_message_text('Услуги не работают в принципе для частных каналов', user_id, message_id, reply_markup=return_keyboard)
            await message.delete()
        else:
            try:
                link = 'https://t.me/' + message.forward_from_chat.username + '/' + str(message.forward_from_message_id)
                await message.delete()      
                await state.update_data(link=link)            
                await dp.bot.edit_message_text('Введите количество просмотров, которые Вы хотите заказать', user_id, message_id, reply_markup=return_keyboard)
                await States.Test_3K_Views.set()   
            except AttributeError:
                await message.delete()


# ------------------ П О В Т О Р И Т Ь   З А К А З ------------------

@dp.callback_query_handler(text_contains='irepeat:')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    action = call.data.split(':')[1]
    amount = int(call.data.split(':')[2])
    service_id = call.data.split(':')[3]
    money = float(call.data.split(':')[4])
    link = data.get('link')
    link_username = data.get('link_username')
    user = await quick_commands.select_user(call.from_user.id)
    balance = user.balance
    if action == 'subs':
        if round(balance, 2) < money:
            await call.message.edit_text('Недостаточно средств на балансе! Заказ отменён.', reply_markup=return_keyboard)
        else:
            await quick_commands.decrease_user_balance(call.from_user.id, balance, money)
            await quick_commands.updated_at_user(
                        call.from_user.id, datetime.datetime.now())
            sss = await quick_commands.select_settings('subs')
            service_id = sss.service_id
            order = await api_service(service_id, link_username, amount)
            await quick_commands.add_order(str(order), call.from_user.id, 'subs', amount, None, f'от {time_now()} на <b>{amount}</b> подписчиков на пост {link_username}', money, datetime.datetime.now())
            await call.message.edit_text(f'Заказ выполняется! Стоимость - {money}₽. Старт выполнения от 1 до 60 минут.', reply_markup=return_keyboard)
            await state.finish()
            await state.update_data(message_id=call.message.message_id)
    elif action == 'views':
        if round(balance, 2) < money:
            await call.message.edit_text('Недостаточно средств на балансе! Заказ отменён.', reply_markup=return_keyboard)
        else:
            await quick_commands.decrease_user_balance(call.from_user.id, balance, money)
            await quick_commands.updated_at_user(
                        call.from_user.id, datetime.datetime.now())
            sss = await quick_commands.select_settings('views')
            service_id = sss.service_id
            order = await api_service(service_id, link, amount)
            if money == 0:
                await quick_commands.decrease_test_3k(call.from_user.id, user.test_3k, amount)
                await quick_commands.add_order(str(order), call.from_user.id, 'views', amount, None, f'от {time_now()} на <b>{amount}</b> халявных просмотров на пост {link}', money, datetime.datetime.now())
                await call.message.edit_text(f'Заказ выполняется!', reply_markup=return_keyboard)
            else:
                await quick_commands.add_order(str(order), call.from_user.id, 'views', amount, None, f'от {time_now()} на <b>{amount}</b> просмотров на пост {link}', money, datetime.datetime.now())
                await call.message.edit_text(f'Заказ выполняется! Стоимость - {money}₽.', reply_markup=return_keyboard)
            await state.finish()
            await state.update_data(message_id=call.message.message_id)
    elif action == 'reactions':
        if round(balance, 2) < money:
            await call.message.edit_text('Недостаточно средств на балансе! Заказ отменён.', reply_markup=return_keyboard)
        else:
            await quick_commands.decrease_user_balance(call.from_user.id, balance, money)
            await quick_commands.updated_at_user(
                        call.from_user.id, datetime.datetime.now())
            order = await api_service(service_id, link, amount)
            await quick_commands.add_order(str(order), call.from_user.id, 'reactions', amount, service_id, f'от {time_now()} на <b>{amount}</b> реакций {rct[f"{service_id}"]} на пост {link}', money, datetime.datetime.now())
            await call.message.edit_text(f'Заказ выполняется! Стоимость - {money}₽. Старт выполнения от 1 до 60 минут.', reply_markup=return_keyboard)
            await state.finish()
            await state.update_data(message_id=call.message.message_id)



@dp.callback_query_handler(text_contains='repeat:')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    action = call.data.split(':')[1]
    amount = int(call.data.split(':')[2])
    service_id = call.data.split(':')[3]
    money = float(call.data.split(':')[4])
    await state.update_data(
        message_id=call.message.message_id,
        action=action,
        amount=amount,
        service_id=service_id,
        money=money
        )
    if action == 'subs':
        await call.message.edit_text('Перешлите в чат любой пост того канала, на который Вы хотите привлечь подписчиков', reply_markup=return_keyboard)
        await States.Repeat.set()
    elif action == 'reactions':
        await call.message.edit_text('Перешлите в чат тот пост, на который Вы хотите выбранные реакции', reply_markup=return_keyboard)
        await States.Repeat.set()
    elif action == 'views':
        await call.message.edit_text('Перешлите в чат тот пост, на который Вы хотите выбранное количество просмотров', reply_markup=return_keyboard)
        await States.Repeat.set()





@dp.message_handler(state=States.Repeat, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    if message.forward_from_message_id is None:
        await message.delete()
    else:
        if message.forward_from_chat.username is None:
            await dp.bot.edit_message_text('Услуги не работают в принципе для частных каналов', user_id, message_id, reply_markup=return_keyboard)
            await message.delete()
        else:
            link = 'https://t.me/' + message.forward_from_chat.username + '/' +str(message.forward_from_message_id)
            link_username = 'https://t.me/' + message.forward_from_chat.username
            await message.delete()
            action = data.get("action")
            amount = data.get("amount")
            service_id = data.get("service_id")
            money = data.get("money")
            user = await quick_commands.select_user(user_id)
            balance = user.balance
            if action == 'subs':
                if round(balance, 2) < money:
                    await dp.bot.edit_message_text('Недостаточно средств на балансе! Заказ отменён.', user_id, message_id, reply_markup=return_keyboard)
                else:
                    await quick_commands.decrease_user_balance(user_id, balance, money)
                    await quick_commands.updated_at_user(
                        user_id, datetime.datetime.now())
                    sss = await quick_commands.select_settings('subs')
                    service_id = sss.service_id
                    order = await api_service(service_id, link_username, amount)
                    await quick_commands.add_order(str(order), user_id, 'subs', amount, None, f'от {time_now()} на <b>{amount}</b> подписчиков на пост {link_username}', money, datetime.datetime.now())
                    await dp.bot.edit_message_text(f'Заказ выполняется! Стоимость - {money}₽. Старт выполнения от 1 до 60 минут.', user_id, message_id, reply_markup=return_keyboard)
                    await state.finish()
                    await state.update_data(message_id=message_id)
            elif action == 'views':
                if round(balance, 2) < money:
                    await dp.bot.edit_message_text('Недостаточно средств на балансе! Заказ отменён.', user_id, message_id, reply_markup=return_keyboard)
                else:
                    await quick_commands.decrease_user_balance(user_id, balance, money)
                    await quick_commands.updated_at_user(
                        user_id, datetime.datetime.now())
                    sss = await quick_commands.select_settings('views')
                    service_id = sss.service_id
                    order = await api_service(service_id, link, amount)
                    if money == 0:
                        await quick_commands.decrease_test_3k(user_id, user.test_3k, amount)
                        await quick_commands.add_order(str(order), user_id, 'views', amount, None, f'от {time_now()} на <b>{amount}</b> халявных просмотров на пост {link}', money, datetime.datetime.now())
                        await dp.bot.edit_message_text(f'Заказ выполняется!', user_id, message_id, reply_markup=return_keyboard)
                    else:
                        await quick_commands.add_order(str(order), user_id, 'views', amount, None, f'от {time_now()} на <b>{amount}</b> просмотров на пост {link}', money, datetime.datetime.now())
                        await dp.bot.edit_message_text(f'Заказ выполняется! Стоимость - {money}₽.', user_id, message_id, reply_markup=return_keyboard)
                    await state.finish()
                    await state.update_data(message_id=message_id)
            elif action == 'reactions':
                if round(balance, 2) < money:
                    await dp.bot.edit_message_text('Недостаточно средств на балансе! Заказ отменён.', user_id, message_id, reply_markup=return_keyboard)
                else:
                    await quick_commands.decrease_user_balance(user_id, balance, money)
                    await quick_commands.updated_at_user(
                        user_id, datetime.datetime.now())
                    order = await api_service(service_id, link, amount)
                    await quick_commands.add_order(str(order), user_id, 'reactions', amount, service_id, f'от {time_now()} на <b>{amount}</b> реакций {rct[f"{service_id}"]} на пост {link}', money, datetime.datetime.now())
                    await dp.bot.edit_message_text(f'Заказ выполняется! Стоимость - {money}₽. Старт выполнения от 1 до 60 минут.', user_id, message_id, reply_markup=return_keyboard)
                    await state.finish()
                    await state.update_data(message_id=message_id)


# ------------------ А В Т О П Р О Д В И Ж Е Н И Е ------------------


@dp.callback_query_handler(text='auto')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text('Автопродвижение - это когда без Вашего участия на каждый новый пост Вашего канала автоматически начисляется заданное Вами заранее количество просмотров. Списываться с баланса стоимость заказов будет также автоматически.', reply_markup=auto_buttons_keyboard)


@dp.callback_query_handler(text='auto_connect')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text('Если хотите подключить данную услугу, то Вам нужно сейчас переслать любой пост Вашего канала сюда.', reply_markup=return_keyboard)
    await States.Auto_Link.set()


@dp.callback_query_handler(text='auto_disconnect')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    autos = await quick_commands.select_auto_user_id(call.from_user.id)
    msg = 'На данный момент у Вас следующие подключенные услуги автопродвижения:\n\n'
    for auto in range(len(autos)):
        if autos[auto].service == 'views':
            msg += f'{auto+1}. Канал t.me/{autos[auto].username}, по {autos[auto].amount} просмотров на пост\n\n'
    if msg == 'На данный момент у Вас следующие подключенные услуги автопродвижения:\n\n':
        msg = 'У Вас нет подключенных услуг автопродвижения'
        await call.message.edit_text(msg, reply_markup=return_keyboard)
    else:
        markup = await markup_disconnect(autos)
        msg += 'Чтобы отключить услугу автопродвижения, нажмите на кнопку с соответствующим её порядковым номером'
        await call.message.edit_text(msg, reply_markup=markup)


@dp.callback_query_handler(text_contains='auto_id:')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    auto = await quick_commands.delete_auto_id(int(call.data.split(':')[-1]))
    await call.message.edit_text('Услуга отключена', reply_markup=return_keyboard)


@dp.callback_query_handler(text='check_auto')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    autos = await quick_commands.select_auto_user_id(call.from_user.id)
    msg = 'На данный момент у Вас следующие подключенные услуги автопродвижения:\n\n'
    for auto in range(len(autos)):
        if autos[auto].service == 'views':
            msg += f'{auto+1}. Канал t.me/{autos[auto].username}, по {autos[auto].amount} просмотров на пост\n\n'
    if msg == 'На данный момент у Вас следующие подключенные услуги автопродвижения:\n\n':
        msg = 'У Вас нет подключенных услуг автопродвижения'
    await call.message.edit_text(msg, reply_markup=return_keyboard)


@dp.message_handler(state=States.Auto_Link, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    if message.forward_from_message_id is None:
        await message.delete()
    else:
        if message.forward_from_chat.username is None:
            await dp.bot.edit_message_text('Услуги не работают в принципе для частных каналов', user_id, message_id, reply_markup=return_keyboard)
            await message.delete()
        else:
            await state.update_data(username=message.forward_from_chat.username)
            await message.delete()
            await dp.bot.edit_message_text('Теперь Вам нужно добавить этого бота в администраторы своего канала. Жмите по кнопке ниже, когда добавите', user_id, message_id, reply_markup=auto_keyboard)


@dp.callback_query_handler(state=States.Auto_Link, text='bot')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    data = await state.get_data()
    username = data.get('username')
    try:
        admins = await dp.bot.get_chat_administrators('@'+username)
        await call.message.edit_text('Отлично. Бот добавлен. Введите количество просмотров, которые Вы хотите заказать', 
            reply_markup=cancel_keyboard)
        await States.Auto_Views.set()
    except ChatNotFound:
        await call.message.edit_text('Будьте внимательны! Вы пока ещё не добавили бота в администраторы.', reply_markup=auto_keyboard)


@dp.message_handler(state=States.Auto_Views, content_types=ContentType.ANY)
async def button(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    try:
        amount = int(message.text)
        await message.delete()
        if amount < 100:
            await dp.bot.edit_message_text("Минимальное количество просмотров - 100", user_id, message_id, reply_markup=cancel_keyboard)
        else:
            username = data.get('username')
            await quick_commands.add_auto(id=random.randint(1, 10000000), username=username, user_id=user_id, service='views', amount=amount)
            await dp.bot.edit_message_text('Услуга автопродвижения успешно подключена!', user_id, message_id, reply_markup=return_keyboard)
            await state.finish()
            await state.update_data(message_id=message_id)
            
    except ValueError:
        await message.delete()
        await dp.bot.edit_message_text("Неверное значение, введите число", user_id, message_id, reply_markup=cancel_keyboard)


@dp.channel_post_handler()
async def button(message: Message):
    auto = await quick_commands.select_auto_username(username=message.chat.username)
    link = 'https://t.me/' + message.chat.username + '/' + str(message.message_id)
    for au in auto:
        if au.service == 'views':
            user = await quick_commands.select_user(au.user_id)
            balance = user.balance
            money = round((au.amount * 0.003), 2)
            if round(balance, 2) < money:
                pass
            else:
                await quick_commands.decrease_user_balance(au.user_id, balance, money)
                await quick_commands.updated_at_user(au.user_id, datetime.datetime.now())
                sss = await quick_commands.select_settings('views')
                service_id = sss.service_id
                order = await api_service(service_id, str(link), int(au.amount))
                # await dp.bot.send_message(au.user_id, order)
                await quick_commands.add_order(str(order), au.user_id, 'views', au.amount, None, f'от {time_now()} на <b>{au.amount}</b> просмотров на пост {link}', money, datetime.datetime.now())


# ------------------------ П Р А Й С --------------------------


@dp.callback_query_handler(text='price')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('''Прайс:\n1000 подписчиков - 250₽\n1000 реакций - 200₽\n1000 просмотров поста - 3₽''', 
        reply_markup=prices_keyboard)


@dp.callback_query_handler(text='views_price')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(
        '1000 просмотров поста - 3₽',
        parse_mode='html', reply_markup=return_keyboard
    )

@dp.callback_query_handler(text='subs_price')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(
        '1000 подписчиков - 250₽',
        parse_mode='html', reply_markup=return_keyboard
    )

@dp.callback_query_handler(text='reactions_price')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text(
        '1000 реакций - 200₽',
        parse_mode='html', reply_markup=return_keyboard
    )


# --------------------- И Н С Т Р У К Ц И Я --------------------


@dp.callback_query_handler(text='instruction')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Канал для продвижения должен быть публичным. Для любой услуги, вы должны переслать пост канала, даже для подписчиков.', reply_markup=return_keyboard)


# ---------------------- П О Д Д Е Р Ж К А ---------------------


@dp.callback_query_handler(text='support')
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Поддержка - @ToolSupports', reply_markup=return_keyboard)


# ------------------- О Т С Л Е Д И Т Ь   З А К А З Ы ---------------------


@dp.callback_query_handler(text='tracking')
async def button(call: CallbackQuery, state: FSMContext):
    orders = await quick_commands.select_orders_by_user(call.from_user.id)
    msg_text = '<b>Показывается последние 10 заказов</b>\n\n'
    msg_error = 'Один или несколько из Ваших заказов были отменены. Деньги возвращены на баланс. Это сообщение автоматически удалится через 10 секунд'
    cancelled_orders = []
    if orders is None or orders == []:
        msg_text += 'У Вас не было заказов.'
    else:
        sorted_orders_ids = quick_commands.sorted_orders(orders, 'created_at')
        sorted_orders = []
        if sorted_orders_ids != []:
            for order_id in sorted_orders_ids:
                sorted_orders.append(await quick_commands.select_order_by_order_id(order_id))
        for order in sorted_orders[-10:]:
            previous_status = order.status
            status = await api_status(order.order_id)
            if status == 'Canceled' and status != previous_status:
                cancelled_orders.append(order)
            msg_text += f'Заказ {order.description}\nСтатус: {status}\n\n'
            # await quick_commands.update_order_status(order.order_id, status)
    await call.answer()
    await call.message.edit_text(msg_text, parse_mode='html', disable_web_page_preview=True, reply_markup=return_keyboard)
    if cancelled_orders != []:
        for order in cancelled_orders:
            user = await quick_commands.select_user(call.from_user.id)
            previous_balance = user.balance
            await quick_commands.increase_user_balance(call.from_user.id, previous_balance, order.money)
        await asyncio.sleep(2)
        msg = await call.message.answer(msg_error)
        await asyncio.sleep(10)
        await dp.bot.delete_message(call.from_user.id, msg.message_id)


# --------- О Б Щ И Е   Н А С Т Р О Й К И   ( К О М А Н Д Ы ) -------------


@dp.callback_query_handler(state='*', text='cancel')
async def cancel_payment(call: CallbackQuery, state: FSMContext):
    await call.answer()
    user = await quick_commands.select_user(call.from_user.id)
    if call.from_user.id in [1247122892, 1048524289, 83335761]:
        if user.test_3k > 0:
            msg = await call.message.edit_text('Этот бот увеличивает количество подписчиков и просмотров на постах в телеграм-пабликах', reply_markup=main_keyboard_VIP_test)
        else:
            msg = await call.message.edit_text('Этот бот увеличивает количество подписчиков и просмотров на постах в телеграм-пабликах', reply_markup=main_keyboard_VIP)
    else:
        if user.test_3k > 0:
            msg = await call.message.edit_text('Этот бот увеличивает количество подписчиков и просмотров на постах в телеграм-пабликах', reply_markup=main_keyboard_test)
        else:
            msg = await call.message.edit_text('Этот бот увеличивает количество подписчиков и просмотров на постах в телеграм-пабликах', reply_markup=main_keyboard)

    await state.finish()
    await state.update_data(message_id=call.message.message_id)


@dp.message_handler(content_types=ContentType.ANY)
async def cancel_payment(message: Message, state: FSMContext):
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    if message.forward_from_message_id is None:
        if message.text != '/start':
            await message.delete()
    else:
        if message.forward_from_chat.username is None:
            await dp.bot.edit_message_text('Услуги не работают в принципе для частных каналов', user_id, message_id, reply_markup=return_keyboard)
            await message.delete()
        else:
            link = 'https://t.me/' + message.forward_from_chat.username + '/' + str(message.forward_from_message_id)
            link_username = 'https://t.me/' + message.forward_from_chat.username
            await message.delete()
            user = await quick_commands.select_user(user_id)
            await state.update_data(link=link, link_username=link_username)

            orders = await quick_commands.select_orders_by_user(user.user_id)
            sorted_orders_ids = quick_commands.sorted_orders(orders, 'created_at')
            sorted_orders = []
            if sorted_orders_ids != []:
                for order_id in sorted_orders_ids:
                    sorted_orders.append(await quick_commands.select_order_by_order_id(order_id))
                
                services_keyboard_last_order_instant = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Просмотры", callback_data="views_instant"),
                    InlineKeyboardButton(text="Подписчики", callback_data="subs_instant"),
                    InlineKeyboardButton(text="Реакции", callback_data="reactions_instant")],
                    [InlineKeyboardButton(text="Повторить заказ ↩️", callback_data=f"irepeat:{sorted_orders[-1].action}:{sorted_orders[-1].amount}:{sorted_orders[-1].service_id}:{sorted_orders[-1].money}")],
                    [InlineKeyboardButton(text="Главное меню 📁", callback_data="cancel")]
                ])  
            if orders == []:
                await dp.bot.edit_message_text("Выберите заказ по продвижению", user_id, message_id, reply_markup=services_keyboard_instant)
            else:
                if sorted_orders[-1].action == 'reactions':
                    await dp.bot.edit_message_text(f'Выберите заказ по продвижению\n\nP.S. Вы также можете повторить последний заказ: <b>{sorted_orders[-1].amount} реакций</b> {rct[f"{sorted_orders[-1].service_id}"]}', user_id, message_id, reply_markup=services_keyboard_last_order_instant)
                elif sorted_orders[-1].action == 'views':
                    await dp.bot.edit_message_text(f'Выберите заказ по продвижению\n\nP.S. Вы также можете повторить последний заказ: <b>{sorted_orders[-1].amount} просмотров</b>', user_id, message_id, reply_markup=services_keyboard_last_order_instant)
                elif sorted_orders[-1].action == 'subs':
                    await dp.bot.edit_message_text(f'Выберите заказ по продвижению\n\nP.S. Вы также можете повторить последний заказ: <b>{sorted_orders[-1].amount} подписчиков</b>', user_id, message_id, reply_markup=services_keyboard_last_order_instant)


@dp.callback_query_handler(text='commands')
async def frhefh(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Какую команду выберете?', 
        reply_markup=commands_keyboard)


@dp.callback_query_handler(text='mailing_all')
async def frhefh(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(message_id=call.message.message_id)
    await call.message.edit_text('Пишите сообщение, которое собираетесь разослать всем пользователям бота.')
    await States.Send_All.set()


@dp.message_handler(state=States.Send_All)
async def frhefh(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    message_id = data.get("message_id")
    user_id = message.from_user.id
    await message.delete()
    await dp.bot.edit_message_text('Подтверждаете выбранный текст?', 
        user_id, message_id, reply_markup=confirm_keyboard)
    await States.Confirm_All.set()


@dp.callback_query_handler(text='confirm', state=States.Confirm_All)
async def button(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Сообщение рассылается...')
    await asyncio.sleep(3)
    ids = await quick_commands.users_ids_all()
    data = await state.get_data()
    text = data.get('text')
    for id in ids:
        try:
            await dp.bot.send_message(id, text)
        except BotBlocked:
            pass
    await call.message.edit_text('Сообщение разослано!', 
        reply_markup=return_keyboard)
    await state.finish()
    await state.update_data(message_id=call.message.message_id)


@dp.callback_query_handler(text='statistics')
async def frhefh(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Какую статистику выберете?', 
        reply_markup=statistics_keyboard)


@dp.callback_query_handler(text='today')
async def frhefh(call: CallbackQuery, state: FSMContext):
    users = await quick_commands.view_all_users()
    msg = f'<b>Всего ботом пользуются {len(users)} человек.\n\n</b>'
    msg_new = ''
    users_today = 0
    for user in users:
        money = 0
        orders = await quick_commands.select_orders_by_user(user.user_id)
        for order in orders:
            money += order.money
        if user.created_at.date() == datetime.datetime.today().date():
            users_today += 1
            if users_today == 51:
                break
            if user.username is None:
                msg_new += f'ID: {user.user_id}\nНикнейм: {user.fullname}\nБаланс: <b>{round(user.balance, 2)}₽</b>\nЗаказы: <b>{round(money, 2)}₽</b>\n\n'
            else:
                msg_new += f'ID: {user.user_id}\nUsername: @{user.username}\nНикнейм: {user.fullname}\nБаланс: <b>{round(user.balance, 2)}₽</b>\nЗаказы: <b>{round(money, 2)}₽</b>\n\n'
    if users_today > 0:
        msg += f'<b>Сегодня добавилось {users_today} человек.\n\nПоказывается не более 50 пользователей:</b>\n\n'
    else:
        msg_new = 'Пользователи в выбранный отрезок времени не добавлялись'
    await call.answer()
    await call.message.edit_text(msg+msg_new, parse_mode='html', 
        reply_markup=commands_return_keyboard)


@dp.callback_query_handler(text='yesterday')
async def frhefh(call: CallbackQuery, state: FSMContext):
    users = await quick_commands.view_all_users()
    msg = f'<b>Всего ботом пользуются {len(users)} человек.\n\n</b>'
    msg_new = ''
    users_yesterday = 0
    for user in users:
        money = 0
        orders = await quick_commands.select_orders_by_user(user.user_id)
        for order in orders:
            money += order.money
        if user.created_at.date() == datetime.datetime.today().date()-datetime.timedelta(days=1):
            users_yesterday += 1
            if users_yesterday == 51:
                break
            if user.username is None:
                msg_new += f'ID: {user.user_id}\nНикнейм: {user.fullname}\nБаланс: <b>{round(user.balance, 2)}₽</b>\nЗаказы: <b>{round(money, 2)}₽</b>\n\n'
            else:
                msg_new += f'ID: {user.user_id}\nUsername: @{user.username}\nНикнейм: {user.fullname}\nБаланс: <b>{round(user.balance, 2)}₽</b>\nЗаказы: <b>{round(money, 2)}₽</b>\n\n'
    if users_yesterday > 0:
        msg += f'<b>Вчера добавилось {users_yesterday} человек.\n\nПоказывается не более 50 пользователей:</b>\n\n'
    else:
        msg_new = 'Пользователи в выбранный отрезок времени не добавлялись'
    await call.answer()
    await call.message.edit_text(msg+msg_new, parse_mode='html', 
        reply_markup=commands_return_keyboard)
        

@dp.callback_query_handler(text='3days')
async def frhefh(call: CallbackQuery, state: FSMContext):
    users = await quick_commands.view_all_users()
    msg = f'<b>Всего ботом пользуются {len(users)} человек.\n\n</b>'
    msg_new = ''
    users_3days = 0
    for user in users:
        money = 0
        orders = await quick_commands.select_orders_by_user(user.user_id)
        for order in orders:
            money += order.money
        if user.created_at.date() >= datetime.datetime.today().date()-datetime.timedelta(days=2):
            users_3days += 1
            if users_3days == 51:
                break
            if user.username is None:
                msg_new += f'ID: {user.user_id}\nНикнейм: {user.fullname}\nБаланс: <b>{round(user.balance, 2)}₽</b>\nЗаказы: <b>{round(money, 2)}₽</b>\n\n'
            else:
                msg_new += f'ID: {user.user_id}\nUsername: @{user.username}\nНикнейм: {user.fullname}\nБаланс: <b>{round(user.balance, 2)}₽</b>\nЗаказы: <b>{round(money, 2)}₽</b>\n\n'
    if users_3days > 0:
        msg += f'<b>За последние 3 дня добавилось {users_3days} человек.\n\nПоказывается не более 50 пользователей:</b>\n\n'
    else:
        msg_new = 'Пользователи в выбранный отрезок времени не добавлялись'
    await call.answer()
    await call.message.edit_text(msg+msg_new, parse_mode='html', 
        reply_markup=commands_return_keyboard)
        

@dp.callback_query_handler(text='active')
async def frhefh(call: CallbackQuery, state: FSMContext):
    users_q = await quick_commands.view_all_users()
    msg = f'<b>Всего ботом пользуются {len(users_q)} человек.\n\n</b>'
    msg_new = ''
    users_active = 0
    sorted_users_ids = quick_commands.sorted_users(users_q, 'updated_at')
    users = []
    if sorted_users_ids != []:
        for user_id in sorted_users_ids:
            users.append(await quick_commands.select_user(int(user_id)))
    for user in users:
        money = 0
        orders = await quick_commands.select_orders_by_user(user.user_id)
        for order in orders:
            money += order.money
        if user.balance != 0:
            users_active += 1
            if users_active == 51:
                break
            if user.username is None:
                msg_new += f'ID: {user.user_id}\nНикнейм: {user.fullname}\nБаланс: <b>{round(user.balance, 2)}₽</b>\nЗаказы: <b>{round(money, 2)}₽</b>\n\n'
            else:
                msg_new += f'ID: {user.user_id}\nUsername: @{user.username}\nНикнейм: {user.fullname}\nБаланс: <b>{round(user.balance, 2)}₽</b>\nЗаказы: <b>{round(money, 2)}₽</b>\n\n'  
    if users_active > 0:
        msg += f'<b>Активных пользователей: {users_active}.\n\nПоказывается не более 50 пользователей:</b>\n\n'
    else:
        msg_new = 'Активных пользователей не найдено'
    await call.answer()
    await call.message.edit_text(msg+msg_new, parse_mode='html', 
        reply_markup=commands_return_keyboard)