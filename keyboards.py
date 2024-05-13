from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def kb_product_catalog(product_id, state, count_products) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    ib1 = InlineKeyboardButton(text='🛒 Заказать', callback_data=f'buy_catalog|{product_id}')
    ib2 = InlineKeyboardButton(text='🗑 В корзину', callback_data=f'basket_catalog|{product_id}')
    count = InlineKeyboardButton(text=f'{state}/{count_products}', callback_data='void')
    forward = InlineKeyboardButton(text='▶️', callback_data=f'forward_product_catalog|{state}')
    back = InlineKeyboardButton(text='◀️', callback_data=f'back_product_catalog|{state}')
    replenish = InlineKeyboardButton(text='💳 Пополнить баланс', callback_data='menu_replenish')
    menu = InlineKeyboardButton(text='🔙 Вернуться в меню', callback_data='back_to_menu')
    return ikb.add(ib1).add(back, count, forward).add(replenish).add(menu)
