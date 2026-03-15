import os
import asyncio
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.core.ml_service import ml_service
from bot.handlers.states import PhotoTextStates

router = Router()


@router.message(Command("photo_to_text"))
async def cmd_photo_to_photo_to_text(message: types.Message, state: FSMContext):
    await state.set_state(PhotoTextStates.waiting_for_photo)
    await message.answer(
        "Для распознавания текста пришлите фотографию.\n"
        "Поддерживаются: русский и английский языки ."
    )


@router.message(PhotoTextStates.waiting_for_photo, F.photo)
async def handle_photo_for_ocr(message: types.Message, state: FSMContext):
    "Обработка фотографии для OCR."
    photo = message.photo[-1]
    file_id = photo.file_id
    file_path = f"temp/{file_id}.jpg"
    os.makedirs("temp", exist_ok=True)
    await message.answer("Распознаю текст с фото 🔄")
    try:
        await message.bot.download(file_id, destination=file_path)
        text = await asyncio.to_thread(ml_service.ocr_predict, file_path)
        if text and len(text) > 0:
            await message.answer(f"Распознанный текст:\n\n{text}")
        else:
            await message.answer(
                "❌ Текст не найден на изображении.\n"
                "Убедитесь, что на фото есть чёткий текст."
            )
        await state.clear()
    except FileNotFoundError:
        await message.answer(
            " ❌ Ошибка: файл не найден.\n" "Попробуйте отправить фото ещё раз."
        )
    except PermissionError:
        await message.answer(
            " ❌ Ошибка: нет доступ а к файлу.\n" "Попробуйте отправить фото ещё раз."
        )
    except Exception:
        await message.answer("Попробуйте отправить другое фото.")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
