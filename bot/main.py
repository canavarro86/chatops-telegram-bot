import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
import jwt

from config.config import SETTINGS
from bot.handlers.commands import register_handlers

# Настройка логирования по стандарту: уровень INFO, формат сообщений можно дополнить при необходимости
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def verify_jwt(token: str) -> dict | None:
    """
    Проверка JWT-токена.

    :param token: строка JWT
    :return: полезная нагрузка из токена или None, если проверка не прошла
    """
    try:
        payload = jwt.decode(
            token,
            SETTINGS.jwt_secret,
            algorithms=["HS256"],
            options={"require_exp": False},  # при необходимости требовать exp
        )
        return payload
    except jwt.PyJWTError as exc:
        logger.warning("Ошибка при верификации JWT: %s", exc)
        return None


async def cmd_start(message: Message) -> None:
    """
    Обработчик команды /start.

    Отправляет приветственное сообщение пользователю.
    """
    await message.answer("Привет! Я ChatOps бот. Введите /help для списка команд.")


async def cmd_help(message: Message) -> None:
    """
    Обработчик команды /help.

    Перечисляет доступные команды бота.
    """
    help_text = (
        "Доступные команды:\n"
        "/issues — показать открытые задачи\n"
        "/workflows — показать workflows CI/CD\n"
        "/build <токен> <id> — запустить workflow\n"
        "/status <токен> <id> — статус последнего run\n"
        "/comment <токен> <номер> <текст> — добавить комментарий к Issue"
    )
    await message.answer(help_text)


async def main() -> None:
    """
    Точка входа приложения.

    Инициализирует бота, диспетчер и запускает polling.
    """
    # Создаём экземпляр Bot и Dispatcher внутри main,
    # чтобы при импорте этого модуля не происходило сетевых операций
    bot = Bot(token=SETTINGS.telegram_token)
    dp = Dispatcher()

    # Регистрируем базовые обработчики
    dp.message.register(cmd_start, Command(commands=["start"]))
    dp.message.register(cmd_help, Command(commands=["help"]))

    # Регистрируем остальные команды из модуля handlers
    register_handlers(dp, verify_jwt)

    logger.info("Запуск бота...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    # Запускаем асинхронный main через asyncio
    import asyncio

    asyncio.run(main())
