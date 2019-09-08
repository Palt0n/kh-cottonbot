"""
This is a echo bot.
It echoes any incoming text messages.
"""

import logging
from aiogram import Bot, Dispatcher, executor, types
from Utilities import get_EnvironmentVariable

API_TOKEN = get_EnvironmentVariable('CHATBOT_KEY')
assert API_TOKEN is not None

import asyncio

DELAY=7200

bot=Bot(token=API_TOKEN)
dp=Dispatcher(bot)

@ dp.message_handler(commands=['start','help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi! \ nI'm EchoBot! \ nPowered by aiogram.")


async def update_price():
  pass


def repeat(coro, loop):
    asyncio.ensure_future(coro(), loop=loop)
    loop.call_later(DELAY, repeat, coro, loop)


if __name__ =='__main__':
    loop=asyncio.get_event_loop()
    loop.call_later(DELAY, repeat, update_price, loop)
    executor.start_polling(dp, loop=loop)