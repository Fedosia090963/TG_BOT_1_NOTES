"""Настройка и запуск Telegram-бота."""

import asyncio
import os

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from app.database import Database
from app.handlers import router


async def main() -> None:
    """Подключает бота и начинает обработку сообщений."""
    load_dotenv()
    token = os.getenv("BOT_TOKEN")

    if not token:
        raise RuntimeError("Переменная BOT_TOKEN не найдена. Создайте .env.")

    database = Database("tasks.db")
    database.init_db()
    database.close()

    bot = Bot(token=token)
    dispatcher = Dispatcher()
    dispatcher.include_router(router)

    await dispatcher.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
