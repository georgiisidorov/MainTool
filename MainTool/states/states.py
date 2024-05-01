from aiogram.dispatcher.filters.state import StatesGroup, State


class States(StatesGroup):
    Deposit = State()
    Payment = State()
    Send_All = State()
    Confirm_All = State()
    Views = State()
    Views_Button = State()
    Views_Link = State()
    Subs = State()
    Subs_Link = State()
    Reactions = State()
    Reactions_Link = State()
    Test_3K = State()
    Test_3K_Views = State()
    Auto_Link = State()
    Auto_Views = State()
    Repeat = State()