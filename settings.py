from functools import lru_cache
from typing import final
from decouple import config
from pydantic_settings import BaseSettings, SettingsConfigDict


@final
class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".prod.env", ".dev.env"),  # first search .dev.env, then .prod.env
        env_file_encoding="utf-8",
    )
    bot_token: str = config("BOT_TOKEN")
    cmc_api_key: str = config("CMC_API_KEY")
    cmc_url: str = config("CMC_URL")
    database: str = config("DATABASE")
    check_interval: int = config("CHECK_INTERVAL")


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()
