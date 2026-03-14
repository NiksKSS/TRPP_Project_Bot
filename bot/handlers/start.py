from aiogram import Router, types
from aiogram.filters import Command

router = Router()


@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для работы с картинками.\n\n"
        "Всё, что я умею, можешь посмотреть в команде /help"
    )
