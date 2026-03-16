import asyncio
import uuid
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.core.ml_service import ml_service
from bot.states import AskImageStates
from bot.core.session_manager import session_manager
import logging

router = Router()
logger = logging.getLogger(__name__)


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
    user_id = message.from_user.id
    photo = message.photo[-1]
    file_id = photo.file_id
    image_path = f"temp/vqa_{user_id}_{uuid.uuid4().hex}.jpg"

    try:
        await message.bot.download(file_id, destination=image_path)
        session_manager.add_file(user_id, image_path)
        await state.set_state(AskImageStates.waiting_for_question)
        await message.answer(
            "Фото сохранено ✅\n"
            "Теперь напиши вопрос по этому изображению на английском языке."
        )

    except FileNotFoundError:
        await message.answer(
            "❌ Ошибка: файл изображения не найден.\n"
            "Пожалуйста, отправь фото заново командой /ask_from_image"
        )


@router.message(
    AskImageStates.waiting_for_question,
    lambda msg: msg.text and not msg.text.startswith("/"),
)
async def handle_question_for_vqa(message: types.Message, state: FSMContext):
    """Обработка вопроса."""
    user_id = message.from_user.id
    question = message.text.strip()
    if not session_manager.has_session(user_id):
        await message.answer(
            "Сначала отправь фото!\n" "Используй команду /ask_from_image"
        )
        return
    files = session_manager.get_files(user_id)
    if not files:
        await message.answer("❌ Фото не найдено. Отправь заново.")
        return
    image_path = files[0]
    await message.answer("Уже ищу ответ на твой вопрос 🔄")

    try:
        answer = await asyncio.to_thread(ml_service.vqa_predict, image_path, question)
        if answer and answer.strip():
            await message.answer(f"Вопрос: {question}\n\n" f"Ответ: {answer}")
        else:
            await message.answer(
                "️❌ Не удалось получить ответ. Попробуй другой вопрос."
            )
        await state.clear()

    except Exception as e:
        logger.error(f"VQA error for user {user_id}: {type(e).__name__} - {e}")
        await message.answer(f"Ошибка: {type(e).__name__}")

    finally:
        session_manager.cleanup(user_id)
