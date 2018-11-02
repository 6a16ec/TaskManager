from aiogram import Bot, Dispatcher, executor, types
import config


bot = Bot(token = config.telegram_token)
dp = Dispatcher(bot)



@dp.message_handler(regexp='(^cat[s]?$|puss)')
async def cats(message: types.Message):
    with open('data/cats.jpg', 'rb') as photo:
        await bot.send_photo(message.chat.id, photo, caption='Cats is here 😺',
                             reply_to_message_id=message.message_id)

@dp.message_handler()
async def echo(message: types.Message):
    await bot.send_message(message.chat.id, message.text)
