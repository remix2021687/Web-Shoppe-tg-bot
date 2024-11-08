import os
from types import NoneType

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

from app.auth.authorization import tokenization, refresh_token
from app.fsm.admin_storage import CreateProduct
from app.keyboards.replay_keyboards import login_keyboard, control_keyboard, cancel_keyboard

load_dotenv()
admin_router = Router()
client = AsyncIOMotorClient(os.getenv('MONGODB_URL'))
db = client[f"{os.getenv('MONGODB_DB_NAME')}"]
collections = db[f"{os.getenv('MONGODB_DB_COLLECTIONS')}"]


@admin_router.message(F.text == 'Cancel')
async def cancel(message: Message, state: FSMContext):
    await message.answer('Creating is cancelled.', reply_markup=control_keyboard)
    await state.clear()

@admin_router.message(F.text == 'Create Product')
async def create_product(message: Message, state: FSMContext):
    find_user: dict = await collections.find_one({
        'tg_user_id': message.from_user.id
    })

    tokens: dict = find_user.get('api_token') if find_user else None

    if tokens is not None:
        valid_access_token: bool = tokenization(tokens['access'])
        valid_refresh_token: bool = tokenization(tokens['refresh'])

        if valid_access_token:
            await state.set_state(CreateProduct.name)
            await message.answer('Entry name product', reply_markup=cancel_keyboard)

        elif valid_refresh_token:
            new_token = refresh_token(tokens['refresh'])
            await collections.find_one_and_update({'tg_user_id': message.from_user.id}, {
                '$set': {
                    'api_token.access': new_token
                }
            })

            await message.answer('Try again', reply_markup=control_keyboard)

        else:
            await collections.find_one_and_delete({'tg_user_id': message.from_user.id})
            await message.answer('Authorization Again', reply_markup=login_keyboard)

    else:
        await message.answer('Authorization Again', reply_markup=login_keyboard)


@admin_router.message(CreateProduct.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateProduct.price)
    await message.answer('Entry price product')
