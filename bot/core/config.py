from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Настройки бота."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    telegram_bot_token: str = Field(default="", validation_alias="BOT_TOKEN")
    tesseract_path: str = Field(default="", validation_alias="TESSERACT_PATH")


settings = Settings()
