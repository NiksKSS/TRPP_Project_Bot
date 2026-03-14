from aiogram import Router
from .handlers import start, help, photo_to_text, text_to_photo

router = Router()

router.include_router(start.router)
router.include_router(help.router)
router.include_router(photo_to_text.router)
router.include_router(text_to_photo.router)
