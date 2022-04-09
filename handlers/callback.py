from aiogram import types
from config import bot, dp

@dp.callback_query_handler(lambda func: func.data == "button_call_1")
async def problem_2(call: types.CallbackQuery):
    photo = open("media/problem2.jpg", "rb")
    await bot.send_photo(call.message.chat.id, photo=photo)

    question = "Output:"
    answers = "10 20 Error".split()
    await bot.send_poll(call.message.chat.id,
                        question=question,
                        options=answers,
                        is_anonymous=False,
                        type='quiz',
                        correct_option_id=2,
                        open_period=5,
                        )
