import os
import asyncio
import uuid
from aiogram import Router, types
from aiogram.filters import Command
from bot.core.ml_service import ml_service

router = Router()


@router.message(Command("text_to_photo"))
async def cmd_text_to_photo(message: types.Message):
    await message.answer("Напиши описание картинки, и я её создам.\n\n")


@router.message(lambda msg: msg.text and not msg.text.startswith("/"))
async def handle_prompt_for_generation(message: types.Message):
    """Обработка запроса на генерацию"""
    prompt = message.text.strip()
    output_path = f"temp/gen_{uuid.uuid4().hex}.png"
    os.makedirs("temp", exist_ok=True)
    await message.answer("Генерирую... Это займёт около 5 минут.")
    try:
        result_path = await asyncio.to_thread(
            ml_service.generate_image, prompt, output_path
        )
        with open(result_path, "rb") as image:
            await message.answer_photo(photo=image, caption=f"По запросу: «{prompt}»")
        os.remove(result_path)
    except Exception as e:
        await message.answer(f"Ошибка генерации: {type(e).__name__}\n" f"Детали: {e}")
