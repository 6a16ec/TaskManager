from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import keyboard

bot = Bot(token= "...")
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.", reply_markup = keyboard.Reply().get())

if __name__ == '__main__':
    executor.start_polling(dp)
