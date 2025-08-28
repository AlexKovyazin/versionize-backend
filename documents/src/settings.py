import os
import pathlib

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic_settings import BaseSettings

env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(env_path)


class Settings(BaseSettings):
    base_dir: pathlib.Path = pathlib.Path(__file__).parent.parent.resolve()
    debug: int = os.getenv("DEBUG", 0)
    local: int = os.getenv("LOCAL", 0)
    is_test: int = os.getenv("IS_TEST", 0)
    db_database: SecretStr = os.getenv("POSTGRES_DB")
    db_username: SecretStr = os.getenv("POSTGRES_USER")
    db_password: SecretStr = os.getenv("POSTGRES_PASSWORD")
    db_host: SecretStr = os.getenv("DB_HOST")
    db_port: SecretStr = os.getenv("DB_PORT")


settings = Settings()
