import os
import asyncio
import uuid
from aiogram import Router, types, F
from aiogram.filters import Command
from bot.core.ml_service import ml_service

router = Router()

vqa_sessions = {}


@router.message(Command("ask_from_image"))
async def cmd_ask_from_image(message: types.Message):
    await message.answer(
        "Режим вопросов по изображению!\n\n"
        "1️)Отправь фото\n"
        "2️)Напиши вопрос по этому фото\n\n"
    )


@router.message(F.photo)
async def handle_photo_for_vqa(message: types.Message):
    """Сохранение фото для вопросов."""
    photo = message.photo[-1]
    file_id = photo.file_id
    image_path = f"temp/vqa_{uuid.uuid4().hex}.jpg"
    os.makedirs("temp", exist_ok=True)
    try:
        await message.bot.download(file_id, destination=image_path)
        vqa_sessions[message.from_user.id] = image_path
        await message.answer(
            "Фото сохранено!\n" "Теперь напиши вопрос по этому изображению."
        )
    except FileNotFoundError:
        await message.answer(
            "Ошибка: файл изображения не найден.\n"
            "Пожалуйста, отправь фото заново командой /ask_from_image"
        )
        vqa_sessions.pop(message.from_user.id, None)


@router.message(lambda msg: msg.text and not msg.text.startswith("/"))
async def handle_question_for_vqa(message: types.Message):
    """Обработка вопроса."""
    user_id = message.from_user.id
    question = message.text.strip()
    if user_id not in vqa_sessions:
        await message.answer(
            "Сначала отправь фото!\n" "Используй команду /ask_from_image"
        )
        return
    image_path = vqa_sessions[user_id]
    await message.answer("Уже ищу ответ на твой вопрос...")
    try:
        answer = await asyncio.to_thread(ml_service.vqa_predict, image_path, question)
        await message.answer(f"Вопрос: {question}\n\n" f"Ответ: {answer}")

    except Exception as e:
        await message.answer(f"Ошибка: {type(e).__name__}\n{e}")
