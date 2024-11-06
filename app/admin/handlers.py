import os

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from app.auth.authorization import tokenization
from app.keyboards.replay_keyboards import login_keyboard

load_dotenv()
admin_router = Router()
client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
db = client[f"{os.getenv('MONGODB_DB_NAME')}"]
collections = db[f"{os.getenv('MONGODB_DB_COLLECTIONS')}"]


@admin_router.message(F.text == 'Create Product')
async def create_product(message: Message):
    find_user:dict = await collections.find_one({
        'tg_user_id': message.from_user.id
    })
    tokens:dict = find_user.get('api_token')
    valid_token:bool = tokenization(tokens['access'])

    if valid_token:
        await message.answer('Token is true!')
    else:
        await message.answer('Token is false!', reply_markup=login_keyboard)

