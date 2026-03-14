import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from bot.core.config import settings
from bot.router import router
from bot.core.logging import LoggingMiddleware

logging.basicConfig(level=logging.INFO)

PRIVATE_COMMANDS = [
    types.BotCommand(command="/start", description="Запустить бота"),
    types.BotCommand(command="/help", description="Справка по командам"),
    types.BotCommand(command="/photo_to_text", description="Распознать текст с фото"),
    types.BotCommand(command="/text_to_photo", description="Сгенерировать картинку"),
    types.BotCommand(command="/ask_from_image", description="Вопрос по фото"),
]


async def set_commands(bot: Bot):
    """Регистрирует команды в Telegram"""
    await bot.set_my_commands(PRIVATE_COMMANDS)
    logging.info("Команды зарегистрированы в меню")


async def main():
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()
    dp.message.middleware(LoggingMiddleware())
    dp.include_router(router)
    await set_commands(bot)
    logging.info("Бот запущен!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
