from aiogram.fsm.state import StatesGroup, State


class LoginForm(StatesGroup):
    username = State()
    password = State()

class TokenStorge(StatesGroup):
    token = State()