import os
import pathlib

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # model_config = SettingsConfigDict(env_file="../.env", extra="ignore")

    BASE_DIR: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
    DEBUG: int = os.getenv("DEBUG", 0)
    LOCAL: int = os.getenv("LOCAL", 0)
    IS_TEST: int = os.getenv("IS_TEST", 0)
    DB_URL: SecretStr = os.getenv("DB_URL", "sqlite:///documents/database.db")


settings = Settings()
