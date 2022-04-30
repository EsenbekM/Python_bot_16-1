from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from decouple import config

TOKEN = config("TOKEN")
bot = Bot(TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())

ADMIN = 683673337

URL = "https://pyrhon16bot.herokuapp.com/"
URI = "postgres://ewiathizhmmjlg:2673b3d810d0a76898b0088c4f9eef95a0f14975f0f6da2449bcab6bb8882b5f@ec2-52-18-116-67.eu-west-1.compute.amazonaws.com:5432/ds0dblpnu0sph"