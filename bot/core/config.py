from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки бота."""

    telegram_bot_token: str
    tesseract_path: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
