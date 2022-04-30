from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram import types, Dispatcher
from config import bot, dp, ADMIN

# @dp.message_handler(commands=['mem'])
from database import bot_db, psql_dp
from parser import anime

async def mem(message: types.Message):
    photo = open('photo_2022-04-09_15-00-02.jpg', 'rb')
    bot.send_photo(message.chat.id, photo=photo)






# @dp.message_handler(commands=['start'])
async def hello(message: types.Message):
    id = message.from_user.id
    username = message.from_user.username
    fullname = message.from_user.full_name

    psql_dp.cursor.execute(f"SELECT id FROM users WHERE id = {id}")
    result = psql_dp.cursor.fetchone()

    if not result:
        psql_dp.cursor.execute(f"INSERT INTO users (id, username, fullname) VALUES (%s, %s, %s)",
                               (id, username, fullname))
        psql_dp.db.commit()
        await bot.send_message(message.chat.id, f"Добро пожаловать {message.from_user.full_name}!")
    else:
        await bot.send_message(message.chat.id, "Опять ты?!")

async def get_users(message: types.Message):
    all_users = psql_dp.cursor.execute("SELECT * FROM users")
    result = psql_dp.cursor.fetchall()
    for i in result:
        await message.reply(
            f"ID: {i[0]}\n"
            f"USERNAME: {i[1]}\n"
            f"FULLNAME: {i[2]}\n\n"
        )
    await message.answer(f"COUNT: {len(result)}")




# @dp.message_handler(commands=['quiz'])
async def quiz_1(message: types.Message):
    question = "Какого типа данных не существует в Python?"
    answers = ['int', 'str', 'elif', 'tuple']
    await bot.send_poll(message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=2
                        )

# @dp.message_handler(commands=['problem'])
async def problem_1(message: types.Message):
    murkup = InlineKeyboardMarkup()
    button_call_1 = InlineKeyboardButton(
        "NEXT",
        callback_data="button_call_1"
    )
    murkup.add(button_call_1)

    photo = open("media/problem1.jpg", "rb")
    await bot.send_photo(message.chat.id, photo=photo)

    question = "Output:"
    answers = ["[2, 4]", '[2, 4, 6]', '[2]', '[4]', '[0]', "Error"]
    await bot.send_poll(message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=0,
                        open_period=5,
                        reply_markup=murkup
                        )

# @dp.message_handler(commands=["ban"], commands_prefix="!/")
async def ban(message: types.Message):
    if message.chat.type != "private":
        if message.from_user.id != ADMIN:
            await message.reply("Ты не мой БОСС!")

        if not message.reply_to_message:
            await message.reply("Команда должна быть ответом на сообщение!")

        else:
            await message.bot.delete_message(message.chat.id, message.message_id)
            await message.bot.kick_chat_member(message.chat.id, user_id=message.reply_to_message.from_user.id)
            await bot.send_message(
                message.chat.id,
                f"{message.reply_to_message.from_user.full_name} забанен по воле {message.from_user.full_name}")


    else:
        await message.answer("Это работает только в группах!")

async def show_random_user(message: types.Message):
    await bot_db.sql_command_random(message)


async def parser_anime(message: types.Message):
    data = anime.parser()
    for item in data:
        await bot.send_message(message.chat.id,
                               f"{item['image']}\n{item['title']}\n\n{item['link']}")




def register_hendlers_client(dp: Dispatcher):
    dp.register_message_handler(mem, commands=["mem"])
    dp.register_message_handler(hello, commands=["start"])
    dp.register_message_handler(quiz_1, commands=["quiz"])
    dp.register_message_handler(problem_1, commands=["problem"])
    dp.register_message_handler(ban, commands=["ban"], commands_prefix="!/")
    dp.register_message_handler(show_random_user, commands=["random"])
    dp.register_message_handler(parser_anime, commands=["anime"])
