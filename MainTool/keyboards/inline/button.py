from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard_test = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Баланс 🏦", callback_data='balance'),
        InlineKeyboardButton(text="Заказать 📑", callback_data='order')],
        [InlineKeyboardButton(text="Халявные просмотры 🤩", callback_data="test_3k")],
        [InlineKeyboardButton(text="Автопродвижение 🦾", callback_data="auto")],
        [InlineKeyboardButton(text="Прайс 🧮", callback_data='price'),
        InlineKeyboardButton(text="Инструкция 📝", 
            callback_data='instruction')],
        [InlineKeyboardButton(text="Поддержка 🧑‍💻", callback_data='support')],
        [InlineKeyboardButton(text="Отследить заказы", 
            callback_data='tracking')]
])


main_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Баланс 🏦", callback_data='balance'),
        InlineKeyboardButton(text="Заказать 📑", callback_data='order')],
        [InlineKeyboardButton(text="Автопродвижение 🦾", callback_data="auto")],
        [InlineKeyboardButton(text="Прайс 🧮", callback_data='price'),
        InlineKeyboardButton(text="Инструкция 📝", 
            callback_data='instruction')],
        [InlineKeyboardButton(text="Поддержка 🧑‍💻", callback_data='support')],
        [InlineKeyboardButton(text="Отследить заказы", 
            callback_data='tracking')]
])


main_keyboard_VIP = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Баланс 🏦", callback_data='balance'),
        InlineKeyboardButton(text="Заказать 📑", callback_data='order')],
        [InlineKeyboardButton(text="Автопродвижение 🦾", callback_data="auto")],
        [InlineKeyboardButton(text="Прайс 🧮", callback_data='price'),
        InlineKeyboardButton(text="Инструкция 📝", 
            callback_data='instruction')],
        [InlineKeyboardButton(text="Поддержка 🧑‍💻", callback_data='support')],
        [InlineKeyboardButton(text="Отследить заказы", 
            callback_data='tracking')],
        [InlineKeyboardButton(text="Команды 👾", callback_data='commands')]
])


main_keyboard_VIP_test = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Баланс 🏦", callback_data='balance'),
        InlineKeyboardButton(text="Заказать 📑", callback_data='order')],
        [InlineKeyboardButton(text="Халявные просмотры 🤩", callback_data="test_3k")],
        [InlineKeyboardButton(text="Автопродвижение 🦾", callback_data="auto")],
        [InlineKeyboardButton(text="Прайс 🧮", callback_data='price'),
        InlineKeyboardButton(text="Инструкция 📝", 
            callback_data='instruction')],
        [InlineKeyboardButton(text="Поддержка 🧑‍💻", callback_data='support')],
        [InlineKeyboardButton(text="Отследить заказы", 
            callback_data='tracking')],
        [InlineKeyboardButton(text="Команды 👾", callback_data='commands')]
])


commands_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Разослать сообщение ✉️", 
            callback_data="mailing_all")],
        [InlineKeyboardButton(text="Статистика 📊", 
            callback_data="statistics")],
        [InlineKeyboardButton(
            text="Главное меню 📁", callback_data="cancel")]
])


balance_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Пополнить 💳", callback_data="deposit"),
        InlineKeyboardButton(text="Посмотреть баланс 🔍", 
            callback_data="checkbalance")],
        [InlineKeyboardButton(
            text="Главное меню 📁", callback_data="cancel")]
])

return_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Главное меню 📁", callback_data="cancel")]
])


services_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Просмотры", callback_data="views"),
        InlineKeyboardButton(text="Подписчики", callback_data="subs"),
        InlineKeyboardButton(text="Реакции", callback_data="reactions")],
        [InlineKeyboardButton(text="Главное меню 📁", callback_data="cancel")]
])


services_keyboard_instant = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Просмотры", callback_data="views_instant"),
        InlineKeyboardButton(text="Подписчики", callback_data="subs_instant"),
        InlineKeyboardButton(text="Реакции", callback_data="reactions_instant")],
        [InlineKeyboardButton(text="Главное меню 📁", callback_data="cancel")]
])


auto_buttons_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Проверить подключения", callback_data="check_auto")],
        [InlineKeyboardButton(text="Подключить услугу", callback_data="auto_connect")],
        [InlineKeyboardButton(text="Отключить услугу", callback_data="auto_disconnect")],
        [InlineKeyboardButton(text="Главное меню 📁", callback_data="cancel")]
])


auto_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Бот добавлен ✅", callback_data="bot")],
        [InlineKeyboardButton(text="Отмена 🚫", callback_data="cancel")]
])


cancel_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена 🚫", callback_data="cancel")]
])


reactions_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👍", callback_data="reaction:6571"),
        InlineKeyboardButton(text="👎", callback_data="reaction:6572"),
        InlineKeyboardButton(text="❤️", callback_data="reaction:6573")],
        [InlineKeyboardButton(text="🔥", callback_data="reaction:6574"),
        InlineKeyboardButton(text="🎉", callback_data="reaction:6575"),
        InlineKeyboardButton(text="🤩", callback_data="reaction:6576")],
        [InlineKeyboardButton(text="😱", callback_data="reaction:6577"),
        InlineKeyboardButton(text="😁", callback_data="reaction:6578"),
        InlineKeyboardButton(text="😢", callback_data="reaction:6579")],
        [InlineKeyboardButton(text="💩", callback_data="reaction:6580"),
        InlineKeyboardButton(text="🤮", callback_data="reaction:6581")],
        [InlineKeyboardButton(text="Главное меню 📁", callback_data="cancel")]
])


prices_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Просмотры", callback_data="views_price"),
        InlineKeyboardButton(text="Подписчики", callback_data="subs_price"),
        InlineKeyboardButton(text="Реакции", callback_data="reactions_price")],
        [InlineKeyboardButton(text="Главное меню 📁", callback_data="cancel")]
])


statistics_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="За сегодня", callback_data="today")],
        [InlineKeyboardButton(text="За вчера", callback_data="yesterday")],
        [InlineKeyboardButton(text="За последние 3 дня", 
            callback_data="3days")],
        [InlineKeyboardButton(text="Активные пользователи", 
            callback_data="active")],
        [InlineKeyboardButton(text="Главное меню 📁", callback_data="cancel")]
])


confirm_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отмена 🚫', callback_data="cancel"),
        InlineKeyboardButton(text='Подтвердить ✅', callback_data="confirm")]
])


commands_return_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Назад ⬅️", 
            callback_data="statistics")],
        [InlineKeyboardButton(
            text="Главное меню 📁", callback_data="cancel")]
])


async def markup_pay(invoice):
    markup = InlineKeyboardMarkup(
            inline_keyboard=
            [
                [InlineKeyboardButton(text="Оплатить 💳", url=invoice)],
                [InlineKeyboardButton(text="Отмена 🚫", 
                    callback_data="cancel")],
                [InlineKeyboardButton(text="Подтвердить платёж ✅", callback_data="paid")]
            ]
        )

    return markup


async def markup_disconnect(autos):
    buttons = []
    for auto in range(len(autos)):
        buttons.append([InlineKeyboardButton(text=f"{auto+1}", callback_data=f"auto_id:{autos[auto].id}")])
    buttons.append([InlineKeyboardButton(text="Отмена 🚫", callback_data="cancel")])
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)

    return markup