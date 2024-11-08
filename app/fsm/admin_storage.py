from aiogram.fsm.state import StatesGroup, State

class CreateProduct(StatesGroup):
    name = State()
    price = State()
    description = State()
    state = State()
    stock = State()
    product_info = State()
    sale = State()
