import asyncio
import uuid
import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from bot.core.ml_service import ml_service
from bot.states import TextToPhotoStates
from bot.core.session_manager import session_manager

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("text_to_photo"))
async def cmd_text_to_photo(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    logger.info(f"User {user_id} started /text_to_photo")
    await state.set_state(TextToPhotoStates.waiting_for_prompt)
    await message.answer("Напиши описание картинки, и я её создам ⬇️\n\n")


@router.message(
    TextToPhotoStates.waiting_for_prompt,
    lambda msg: msg.text and not msg.text.startswith("/"),
)
async def handle_prompt_for_generation(message: types.Message, state: FSMContext):
    """Обработка запроса на генерацию"""
    user_id = message.from_user.id
    prompt = message.text.strip()
    output_path = f"temp/gen_{user_id}_{uuid.uuid4().hex}.png"
    logger.info(f"User {user_id} sent prompt: {prompt[:50]}...")
    await message.answer("Генерирую 🔄 Это займёт около 5 минут.")

    try:
        logger.info(f"Starting image generation for user {user_id}: {output_path}")
        result_path = await asyncio.to_thread(ml_service.generate_image, prompt, output_path)
        if session_manager.is_cancelled(user_id):
            logger.info(f"Generation completed but cancelled by user {user_id}, not sending")
            await state.clear()
            return
        logger.info(f"Image generated successfully: {result_path}")
        session_manager.add_file(user_id, result_path)
        image = FSInputFile(result_path)
        await message.answer_photo(photo=image, caption=f"По запросу: «{prompt}»")
        logger.info(f"Image sent to user {user_id}")
        await state.clear()

    except Exception as e:
        logger.error(f"Generation error for user {user_id}: {type(e).__name__} - {e}")
        await message.answer("❌ Ошибка генерации. Попробуйте ещё раз.")

    finally:
        session_manager.cleanup(user_id)
