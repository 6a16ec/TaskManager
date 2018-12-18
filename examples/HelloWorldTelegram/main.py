from aiogram import Bot, types, Dispatcher
from aiogram.utils import executor
import config, keyboard

bot = Bot(token=config.telegram_token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'about'])
async def cats(message: types.Message):
    print("ok")
    await bot.send_message(message.chat.id, "И тебе привет!", reply_markup=keyboard.createInline("BUTTON"))


@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)


executor.start_polling(dp, skip_updates=True)
