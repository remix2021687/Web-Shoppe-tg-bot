from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup

login_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Login')]
])

control_keyboard = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Create Product'), KeyboardButton(text='Edit Product')],
    [KeyboardButton(text='Delete Product'), KeyboardButton(text='Product List')]
], resize_keyboard=True, input_field_placeholder='Select')