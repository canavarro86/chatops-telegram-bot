# bot/main.py

import logging
import jwt

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from config.config import SETTINGS
from bot.handlers.commands import register_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=SETTINGS.telegram_token)
dp = Dispatcher()

# JWT-проверка
def verify_jwt(token: str):
    try:
        return jwt.decode(token, SETTINGS.jwt_secret, algorithms=["HS256"])
    except jwt.PyJWTError:
        return None

# /start
@dp.message(Command("start"))
async def cmd_start(message):
    await message.answer("Привет! Я ChatOps бот. Введите /help для списка команд.")

# Регистрируем остальные команды
register_handlers(dp, verify_jwt)

if __name__ == "__main__":
    dp.run_polling(bot, skip_updates=True)
