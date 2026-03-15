import os
import asyncio
import uuid
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from bot.core.ml_service import ml_service
from bot.handlers.states import TextToPhotoStates

router = Router()


@router.message(Command("text_to_photo"))
async def cmd_text_to_photo(message: types.Message, state: FSMContext):
    await state.set_state(TextToPhotoStates.waiting_for_prompt)
    await message.answer("Напиши описание картинки, и я её создам ⬇️\n\n")


@router.message(TextToPhotoStates.waiting_for_prompt, lambda msg: msg.text and not msg.text.startswith("/"))
async def handle_prompt_for_generation(message: types.Message, state: FSMContext):
    """Обработка запроса на генерацию"""
    prompt = message.text.strip()
    output_path = f"temp/gen_{uuid.uuid4().hex}.png"
    os.makedirs("temp", exist_ok=True)
    await message.answer("Генерирую 🔄 Это займёт около 5 минут.")
    try:
        result_path = await asyncio.to_thread(
            ml_service.generate_image, prompt, output_path
        )
        image = FSInputFile(result_path)
        await message.answer_photo(photo=image, caption=f"По запросу: «{prompt}»")
        os.remove(result_path)
        await state.clear()
    except Exception as e:
        await message.answer(f"Ошибка генерации: {type(e).__name__}\n" f"Детали: {e}")
