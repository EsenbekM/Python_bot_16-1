from aiogram import types, Dispatcher
from config import bot, dp

from lists import bad_words as bw
import asyncio
import aioschedule

async def wake_up():
    video = open("media/erjan.mp4", "rb")
    await bot.send_video(chat_id=chat_id, video=video, caption="Эржан вставай!!!")

async def scheduler(time):
    aioschedule.every().day.at(time).do(wake_up)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)

# @dp.message_handler()
async def echo_message(message: types.Message):
    global chat_id
    chat_id = message.chat.id

    # Check bad words
    bad_words = bw

    for i in bad_words:
        if i in message.text.lower():
            await message.delete()
            await bot.send_message(message.chat.id,
                           f"{message.from_user.full_name}, сам ты {i}!!!"
                           )

    # Send dice
    if message.text.lower() == 'dice':
        await bot.send_dice(message.chat.id, emoji="🎯")

    # notification
    if message.text.startswith("разбуди меня в "):
        await message.reply("ok")
        await scheduler(message.text.replace("разбуди меня в ", ''))


def register_hendlers_notification(dp: Dispatcher):
    dp.register_message_handler(echo_message)