from functools import lru_cache
from pathlib import Path

from pydantic import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=Path(__file__).parent.parent / ".env",
    )

    postgres_url: PostgresDsn
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
