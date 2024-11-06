import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from app.auth.handlers import auth_router
from app.admin.handlers import admin_router
import app.keyboards.replay_keyboards as keyboards

load_dotenv()
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Welcome to Web-Shoppe ADMIN Panel', reply_markup=keyboards.login_keyboard)


async def main():
    dp.include_router(auth_router)
    dp.include_router(admin_router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    if os.getenv('DEBUG'):
        logging.basicConfig(level=logging.INFO)

    asyncio.run(main())
