import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from app.auth.authorization import authorization
import app.keyboards.replay_keyboards as keyboards
from app.fsm.auth_storage import LoginForm

load_dotenv()
auth_router = Router()
client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
db = client[f"{os.getenv('MONGODB_DB_NAME')}"]
collections = db[f"{os.getenv('MONGODB_DB_COLLECTIONS')}"]

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

    login = authorization(data["username"], data["password"])

    if login:
        await message.answer('You are now logged in!', reply_markup=keyboards.control_keyboard)
        await collections.insert_one({
            "tg_user_id": message.from_user.id,
            'tg_username': message.from_user.username,
            'api_token': login
        })
        await state.clear()
    else:
        await message.answer('Invalid username or password!', reply_markup=keyboards.login_keyboard)
        await state.clear()
