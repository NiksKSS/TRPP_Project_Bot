import os
import asyncio
import uuid
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.core.ml_service import ml_service
from bot.handlers.states import AskImageStates

router = Router()

vqa_sessions = {}


@router.message(Command("ask_from_image"))
async def cmd_ask_from_image(message: types.Message, state: FSMContext):
    await state.set_state(AskImageStates.waiting_for_photo)
    await message.answer(
        "Режим вопросов по изображению!\n\n"
        "1️⃣ Отправь фото\n"
        "2️⃣ Напиши вопрос по этому фото\n\n"
    )


@router.message(AskImageStates.waiting_for_photo, F.photo)
async def handle_photo_for_vqa(message: types.Message, state: FSMContext):
    """Сохранение фото для вопросов."""
    photo = message.photo[-1]
    file_id = photo.file_id
    image_path = f"temp/vqa_{uuid.uuid4().hex}.jpg"
    os.makedirs("temp", exist_ok=True)
    try:
        await message.bot.download(file_id, destination=image_path)
        vqa_sessions[message.from_user.id] = image_path
        await state.set_state(AskImageStates.waiting_for_question)
        await message.answer(
            "Фото сохранено ✅\n" "Теперь напиши вопрос по этому изображению."
        )
    except FileNotFoundError:
        await message.answer(
            "❌ Ошибка: файл изображения не найден.\n"
            "Пожалуйста, отправь фото заново командой /ask_from_image"
        )
        vqa_sessions.pop(message.from_user.id, None)


@router.message(AskImageStates.waiting_for_question, lambda msg: msg.text and not msg.text.startswith("/"))
async def handle_question_for_vqa(message: types.Message, state: FSMContext):
    """Обработка вопроса."""
    user_id = message.from_user.id
    question = message.text.strip()
    if user_id not in vqa_sessions:
        await message.answer(
            "Сначала отправь фото!\n" "Используй команду /ask_from_image"
        )
        return
    image_path = vqa_sessions[user_id]
    await message.answer("Уже ищу ответ на твой вопрос 🔄")
    try:
        answer = await asyncio.to_thread(ml_service.vqa_predict, image_path, question)
        await message.answer(f"Вопрос: {question}\n\n" f"Ответ: {answer}")
        vqa_sessions.pop(user_id, None)
        await state.clear()

    except Exception as e:
        await message.answer(f"Ошибка: {type(e).__name__}\n{e}")
