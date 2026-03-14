from aiogram import Router
from .handlers import start, help

router = Router()

router.include_router(start.router)
router.include_router(help.router)
