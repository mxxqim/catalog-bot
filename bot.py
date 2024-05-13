import database as db
import config as cfg
import keyboards as ikb
from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import MessageNotModified
from contextlib import suppress

bot = Bot(token="enter you token")
dp = Dispatcher(bot)


async def on_startup(_):
    from database import connect_database
    connect_database()


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    try:
        chat = message.chat
        count = await db.select_count_products()
        data = await db.select_prodcut_for_rowid(0)  # catalog will start with the first product
        await bot.send_photo(chat.id, photo=data[3], caption=cfg.get_caption(data[2], data[1]),
                             reply_markup=ikb.kb_product_catalog(data[0], 1, count[0]))
    except TypeError:
        await message.answer('Товаров пока что нету')


@dp.callback_query_handler(lambda c: c.data.startswith('forward_product_catalog'))
async def call_forward_product_catalog(call: types.CallbackQuery):
    data_call = call.data.split('|')
    row_id = int(data_call[1])
    count = await db.select_count_products()
    with suppress(MessageNotModified):
        if row_id + 1 > count[0]:
            data = await db.select_prodcut_for_rowid(0)
            await call.message.edit_media(
                types.InputMedia(media=data[3], caption=cfg.get_caption(data[2], data[1])),
                reply_markup=ikb.kb_product_catalog(data[0], 1, count[0]))
        else:
            data = await db.select_prodcut_for_rowid(row_id)
            await call.message.edit_media(
                types.InputMedia(media=data[3], caption=cfg.get_caption(data[2], data[1])),
                reply_markup=ikb.kb_product_catalog(data[0], row_id + 1, count[0]))


@dp.callback_query_handler(lambda c: c.data.startswith('back_product_catalog'))
async def call_back_product_catalog(call: types.CallbackQuery):
    data_call = call.data.split('|')
    row_id = int(data_call[1])
    count = await db.select_count_products()
    with suppress(MessageNotModified):
        if row_id - 1 > 0:
            data = await db.select_prodcut_for_rowid(row_id - 2)
            await call.message.edit_media(types.InputMedia(media=data[3], caption=cfg.get_caption(data[2], data[1])),
                                          reply_markup=ikb.kb_product_catalog(data[0], row_id - 1, count[0]))
        else:
            data = await db.select_prodcut_for_rowid(count[0] - 1)
            await call.message.edit_media(types.InputMedia(media=data[3], caption=cfg.get_caption(data[2], data[1])),
                                          reply_markup=ikb.kb_product_catalog(data[0], count[0], count[0]))


@dp.message_handler(commands='add_product')  # format: /add_prodcut <prduct_price> <product_photo(file_id)> <product_description>
async def cmd_add_product(message: types.Message):
    try:
        product_price = int(message.text.split()[1])
        product_photo = message.text.split()[2]
        product_description = ' '.join(message.text.split()[3:])
        print(product_price, product_photo, product_description)
    except (IndexError, ValueError):
        await message.answer('Incorrect input')
    else:
        await db.insert_product(product_price, product_photo, product_description)
        await message.answer('Successfuly!')


@dp.message_handler(content_types='photo')  # get file_id for product_photo
async def content_types_photo(message: types.Message):
    await message.reply(f'<code>{message.photo[0].file_id}</code>', parse_mode=types.ParseMode.HTML)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
