import os
import asyncio
import time
import logging
import get_post
from aiogram import executor
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import Command
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.set_bot_commands import set_default_commands
from aiogram.utils.exceptions import PhotoDimensions
from aiogram.types.input_media import InputMediaPhoto
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.environ.get("BOT_TOKEN")
LOG = os.environ.get("LOG")
PASS = os.environ.get("PASS")

logging.basicConfig(level=logging.INFO, filename="bot_log.log", filemode="w")

bot = Bot(token = TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
async def on_startup(dispatcher):
    #await set_default_commands(dispatcher)
    scheduler = AsyncIOScheduler
    scheduler.add_job()

@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hi! I will check a new posts in some groups")

@dp.message_handler(Command("help"))
async def cmd_start(message: types.Message):
    text = ("List of commands: ",
            "/start - Start using bot",
            "/help - Get list of commands",
            "/begin - Start checking are there new posts bot",
            "/github - Get link to the github")
    await message.answer("\n".join(text))

@dp.message_handler(Command("github"))
async def cmd_start(message: types.Message):
    text = "Link to the github: https://github.com/IvanSergeevPhysics"
    await message.answer(text)

@dp.message_handler(Command("begin111222"))
async def cmd_begin(message: types.Message):
    user_id = message.from_user.id
    groups = ['public190362085', 'notitle.softgrunge', 'notitle.colorkidcore']
    #, 'notitle.softgrunge', 'notitle.colorkidcore'
    grabber = get_post.VKGrabber(LOG, PASS)
    while True:

        notify_message, img_lst = grabber.checkNewPost(groups)
        mediaGroup = [InputMediaPhoto(media = url) for url in img_lst]

        await bot.send_message(chat_id = user_id, text = notify_message)
        await bot.send_media_group(chat_id = user_id, media = mediaGroup)
        #await bot.send_message(chat_id = user_id, text = notify_message)
        #await message.answer(notify_message)
        time.sleep(30)




async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)