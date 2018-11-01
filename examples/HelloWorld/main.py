from aiogram import Bot, Dispatcher, executor, types
import config.py

def main():

    bot = Bot(token = config.telegram_token)
    dp = Dispatcher(bot)

    @dp.message_handler(commands=['start'])
    @rate_limit(5, 'start')  # this is not required but you can configure throttling manager for current handler using it
    async def cmd_test(message: types.Message):
        # You can use this command every 5 seconds
        await message.reply('Test passed! You can use this command every 5 seconds.')


    @dp.message_handler()
    async def echo(message: types.Message):
        await bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
