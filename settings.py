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
    # BOT_TOKEN = "7289662564:AAElrgEympPGYKakonX00KUcqFYt7G1n46w"
    bot_token: str = config("BOT_TOKEN")
    # CMC_API_KEY = "263b23f4-cff7-487c-b5dc-99ca1f39232c"
    cmc_api_key: str = config("CMC_API_KEY")
    # CMC_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    cmc_url: str = config("CMC_URL")
    # DATABASE = "thresholds.db"
    database: str = config("DATABASE")
    # CHECK_INTERVAL = 60
    check_interval: int = config("CHECK_INTERVAL")


@lru_cache()  # get it from memory
def get_settings() -> Settings:
    return Settings()