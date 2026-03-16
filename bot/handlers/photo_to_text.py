import asyncio
import logging
from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.core.ml_service import ml_service
from bot.core.session_manager import session_manager
from bot.states import PhotoTextStates

router = Router()
logger = logging.getLogger(__name__)


@router.message(Command("photo_to_text"))
async def cmd_photo_to_photo_to_text(message: types.Message, state: FSMContext):
    await state.set_state(PhotoTextStates.waiting_for_photo)
    await message.answer(
        "Для распознавания текста пришлите фотографию.\n"
        "Поддерживаются: русский и английский языки."
    )


@router.message(PhotoTextStates.waiting_for_photo, F.photo)
async def handle_photo_for_ocr(message: types.Message, state: FSMContext):
    """Обработка фотографии для OCR."""
    user_id = message.from_user.id
    photo = message.photo[-1]
    file_id = photo.file_id
    file_path = f"temp/ocr_{user_id}_{file_id}.jpg"
    await message.answer("Распознаю текст с фото 🔄")

    try:
        logger.info(f"User {user_id} sent photo for OCR: {file_path}")
        await message.bot.download(file_id, destination=file_path)
        session_manager.add_file(user_id, file_path)
        logger.info(f"Photo downloaded, starting OCR for user {user_id}")
        text = await asyncio.to_thread(ml_service.ocr_predict, file_path)

        if text and len(text) > 0:
            logger.info(f"OCR successful for user {user_id}, text length: {len(text)}")
            await message.answer(f"Распознанный текст:\n\n{text}")

        else:
            logger.warning(f"No text found in image for user {user_id}")
            await message.answer(
                "❌ Текст не найден на изображении.\n"
                "Убедитесь, что на фото есть чёткий текст."
            )
        await state.clear()
    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError for user {user_id}: {file_path} - {e}")
        await message.answer(
            "❌ Ошибка: файл не найден. Попробуйте отправить фото ещё раз."
        )

    except PermissionError as e:
        logger.error(f"PermissionError for user {user_id}: {file_path} - {e}")
        await message.answer(
            "❌ Ошибка: нет доступа к файлу. Попробуйте отправить фото ещё раз."
        )

    except Exception as e:
        logger.error(f"Unexpected error for user {user_id}: {type(e).__name__} - {e}")
        await message.answer(
            "❌ Произошла ошибка при обработке фото. Попробуйте ещё раз."
        )

    finally:
        session_manager.cleanup(user_id)
