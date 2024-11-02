from aiogram import Router, F
# from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.auth.login import auth_login
import app.keyboards.replay_keyboards as keyboards
from app.fsm.auth import LoginForm

auth_router = Router()


@auth_router.message(F.text == 'Login')
async def start_login(message: Message, state: FSMContext):
    await state.set_state(LoginForm.username)
    await message.answer('Enter your username:')


@auth_router.message(LoginForm.username)
async def set_username(message: Message, state: FSMContext):
    await state.update_data(username=message.text)
    await state.set_state(LoginForm.password)
    await message.answer('Enter your password:')


@auth_router.message(LoginForm.password)
async def set_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    data = await state.get_data()

    login = auth_login(data["username"], data["password"])

    if login:
        await message.answer('You are now logged in!', reply_markup=keyboards.control_keyboard)
        await state.clear()
    else:
        await message.answer('Invalid username or password!', reply_markup=keyboards.login_keyboard)
        await state.clear()
