import logging
import time
from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        start_time = time.time()
        if isinstance(event, Message):
            logger.info(
                f"Пользователь @{event.from_user.username} ({event.from_user.id}) "
                f"отправил: {event.text or 'Фото/Файл'}"
            )
        res = await handler(event, data)
        process_time = time.time() - start_time
        logger.info(f"Обработано за {process_time:.2f} сек")
        return res
