from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🔻 Доступные команды: 🔻\n\n"
        "/start - Запустить бота\n"
        "/help - Показать справку\n"
        "/photo_to_text - Распознавание текста с картинки\n"
        "/text_to_photo - Генерация картинки по описанию\n"
        "/ask_from_image - Вопрос по фото\n"
    )
