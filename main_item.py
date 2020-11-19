from aiogram import executor, Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData
from aiogram.types import CallbackQuery

TOKEN = "TOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKENTOKEN"
bot = Bot(TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


buy_callback = CallbackData("buy", "name", "item_id", "like", "dislike")

#Наприклад я ці данні отримав з бази данних
name_item = "Кактус"
url_photo = "https://images.wallpaperscraft.ru/image/kaktus_sukkulent_rastenie_192805_800x600.jpg"
capture = "Кактус"
item_ids = "9342034"
like = 0
dislike = 0

#Кнопки
kaktus = InlineKeyboardMarkup(row_width=2,
                              inline_keyboard=[
                                  [
                                      InlineKeyboardButton(
                                          text="Купити товар",
                                          callback_data=buy_callback.new(
                                              name=name_item,
                                              item_id=item_ids,
                                              like=like,
                                              dislike=dislike
                                          )
                                      )
                                  ],
                                  [
                                      InlineKeyboardButton(
                                          text="👍",
                                          callback_data=buy_callback.new(
                                              name=name_item,
                                              item_id=item_ids,
                                              like="like",
                                              dislike="."
                                          )
                                      ),
                                      InlineKeyboardButton(
                                          text="👎",
                                          callback_data=buy_callback.new(
                                              name=name_item,
                                              item_id=item_ids,
                                              like=".",
                                              dislike="dislike"
                                          )
                                      )
                                  ],
                                  [
                                      InlineKeyboardButton(
                                          text="Відправити другу",
                                          switch_inline_query="435142119"
                                      )
                                  ]
                                ]
                              )





@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(f'Привіт, {message.from_user.full_name}!')

@dp.message_handler(Command("item"))
async def send_keyboard_item(message: types.Message):
    await message.answer_photo(photo=url_photo, caption=capture, reply_markup=kaktus)



@dp.callback_query_handler(buy_callback.filter(like="like", item_id=item_ids))
async def get_items(call:CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    likes = callback_data.get("like")
    global like
    like = like + 1
    await call.message.answer_photo(photo=url_photo, caption="Тобі сподобався цей товар")

@dp.callback_query_handler(buy_callback.filter(dislike="dislike", item_id=item_ids))
async def get_items(call:CallbackQuery):
    await call.answer(cache_time=1)
    global dislike
    dislike = dislike + 1
    await call.message.answer_photo(photo=url_photo, caption="Тобі не сподобався цей товар")

@dp.callback_query_handler(buy_callback.filter(item_id=item_ids))
async def get_items(call:CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    print("Лайків: "+ str(like))
    print("Дизайків: " + str(dislike))
    kaktus_id = callback_data.get("item_id")
    await call.message.answer_photo(photo=url_photo, caption="Купляй товар №" + str(kaktus_id))






@dp.message_handler()
async def echo(message: types.Message):
    await message.answer("Спробуй використати команду /item. :D")

if __name__ == '__main__':
    executor.start_polling(dp)
