import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class SessionManager:
    """Централизованное управление временными файлами пользователей."""

    def __init__(self, temp_dir: str = "temp"):
        self.temp_dir = Path(temp_dir)
        self.temp_dir.mkdir(exist_ok=True)
        self._sessions: dict[int, dict] = {}

    def add_file(self, user_id: int, file_path: str) -> None:
        """Добавить файл в сессию пользователя."""
        if user_id not in self._sessions:
            self._sessions[user_id] = {"files": [], "cancelled": False}
        self._sessions[user_id]["files"].append(file_path)
        logger.debug(f"Added file to session {user_id}: {file_path}")

    def cancel(self, user_id: int) -> bool:
        """Установить флаг отмены для пользователя."""
        if user_id in self._sessions:
            self._sessions[user_id]["cancelled"] = True
            logger.info(f"Session cancelled for user {user_id}")
            return True
        return False

    def is_cancelled(self, user_id: int) -> bool:
        """Проверить, отменена ли операция."""
        return self._sessions.get(user_id, {}).get("cancelled", False)

    def cleanup(self, user_id: int) -> list[str]:
        """Удалить все временные файлы пользователя."""
        cleaned = []
        if user_id in self._sessions:
            for file_path in self._sessions[user_id]["files"]:
                try:
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        cleaned.append(file_path)
                        logger.debug(f"Deleted temp file: {file_path}")
                except Exception as e:
                    logger.warning(f"Failed to delete {file_path}: {e}")
            del self._sessions[user_id]
        return cleaned

    def cleanup_all(self) -> list[str]:
        """Удалить все временные файлы всех пользователей."""
        all_cleaned = []
        for user_id in list(self._sessions.keys()):
            all_cleaned.extend(self.cleanup(user_id))
        return all_cleaned

    def get_files(self, user_id: int) -> list[str]:
        """Получить список файлов пользователя."""
        return self._sessions.get(user_id, {}).get("files", [])

    def has_session(self, user_id: int) -> bool:
        """Есть ли активная сессия у пользователя."""
        return user_id in self._sessions and len(self._sessions[user_id]["files"]) > 0


session_manager = SessionManager()
