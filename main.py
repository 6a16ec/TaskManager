import asyncio
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import tg_token
from query import query
from generate import generate_all
from timer import event
from objects import Tasks, UnusualTasks
import database
import time
import keyboard

generate = generate_all()
timers = []
constants = database.table("constants").select_all()
constants = {field: value for field, value in constants}
tasks = Tasks()
unusual_tasks = UnusualTasks()

DELAY = 30

bot = Bot(token=tg_token)
dp = Dispatcher(bot)


### --- ### --- ### ---- TASK ---- ### --- ### --- ###

@dp.message_handler(commands=['orf'])
async def new_orf(message: types.Message):
    msg, kb = unusual_tasks.orthoepy(message.chat.id).new()
    # msg = "\n".join([",".join([field for field in line]) for line in database.table("orthoepy").select_all()])
    # msg = [", ".join([str(field) for field in line]) for line in database.table("orthoepy").select_all()]
    # msg = msg[0] + msg[1] + msg[2]
    await message.reply(text=msg, reply_markup=kb, reply=False)

@dp.callback_query_handler(lambda callback_: query(callback_.data, False).effect == "EDIT_MSG_AND_SEND_NEW")
async def new_message(callback: types.CallbackQuery):
    await callback.answer(show_alert=False)
    query_info = query(callback.data)
    msg = database.table("orthoepy").select("description", "id", query_info.word_id)[0][0]
    if query_info.answer == True:
        msg = f"Правильно!\n{msg}"
    else:
        msg = f"Неправильно.\n{msg}"
    await callback.message.edit_text(msg)
    await new_orf(callback.message)



# @dp.callback_query_handler(lambda callback_: query(callback_.data, False).effect == "NEW_MSG")
# async def new_message(callback: types.CallbackQuery):


### --- ### --- ### ---- TEXT MESSAGE ---- ### --- ### --- ###

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


@dp.message_handler(commands=["timer"])
async def send_welcome(message: types.Message):
    msg, kb = generate.new_timer()
    await message.reply(msg, reply_markup=kb, reply=False)


@dp.message_handler(
    func=lambda message: message.reply_to_message and constants["create_task"] in message.reply_to_message.text)
async def send_welcome(message: types.Message):
    task = tasks.new(message.text)
    msg_text, keyboard = task.message(), task.keyboard()
    await message.reply(msg_text, reply_markup=keyboard, reply=False, parse_mode="markdown")


@dp.message_handler()
async def send_welcome(message: types.Message):
    msg, kb = generate.main()
    await message.reply(msg, reply_markup=kb, reply=False)


### --- ### --- ### ---- QUERY MESSAGE ---- ### --- ### --- ###

@dp.callback_query_handler(lambda callback_: query(callback_.data, False).effect == "NEW_MSG")
async def new_message(callback: types.CallbackQuery):
    await callback.answer(show_alert=False)
    query_info = query(callback.data)

    if query_info.module == "main":
        if query_info.event == "timer":
            msg, kb = generate.set_timer()
        elif query_info.event == "create_task":
            msg, kb = constants["create_task"], types.ForceReply()

        else:
            msg, kb = "Not available", None
    else:
        msg, kb = "Not available", None
    new_msg = await callback.message.reply(msg, reply_markup=kb, reply=False)

    if query_info.event == "timer":
        print(query_info.query)
        timers.append([new_msg, event("До конца осталось:\n{time}", int(time.time()) + query_info.duration * 60)])


@dp.callback_query_handler(lambda callback_: query(callback_.data, False).effect == "EDIT_KB")
async def new_message(callback: types.CallbackQuery):
    await callback.answer(show_alert=False)
    # await callback.message.reply(callback.data, reply=False)

    query_info = query(callback.data)

    if query_info.module == "task":
        if query_info.event == "update":
            task = tasks.byid[query_info.task_id]
            task.update(**{query_info.parameter: query_info.value})
            keyboard = task.keyboard()
        elif query_info.event == "keyboard":
            task = tasks.byid[query_info.task_id]
            keyboard = task.keyboard(query_info.type)

    message = callback.message
    user_id, message_id = message.chat.id, message.message_id
    await bot.edit_message_reply_markup(user_id, message_id, None, keyboard)


@dp.callback_query_handler(lambda callback_: query(callback_.data, False).effect == "NOTHING")
async def new_message(callback: types.CallbackQuery):
    await callback.answer(show_alert=False)

@dp.callback_query_handler()
async def new_message(callback: types.CallbackQuery):
    await callback.answer(show_alert=False)
    await callback.message.reply(callback.data, reply=False)


async def update_price():
    print("Hello World")
    for msg, timer in timers:
        await bot.edit_message_text(timer.update(), msg.chat.id, msg.message_id)


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, update_price, loop)
    executor.start_polling(dp, loop=loop, skip_updates=True)

executor.start_polling(dp, skip_updates=True)
