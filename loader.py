from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.db_api import Database


TOKEN = "7711895949:AAH2HobYA2AxDlgmoO8Co-VWLN4XBKk-7F8"
ADMIN = 5235874857
dp = Dispatcher()
baza = Database('database/main.db')
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


