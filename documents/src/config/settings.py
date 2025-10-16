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
    service_host: str = os.getenv("SERVICE_HOST")
    service_port: int = os.getenv("SERVICE_PORT")
    db_database: SecretStr = os.getenv("POSTGRES_DB")
    db_username: SecretStr = os.getenv("POSTGRES_USER")
    db_password: SecretStr = os.getenv("POSTGRES_PASSWORD")
    db_host: SecretStr = os.getenv("DB_HOST")
    db_port: SecretStr = os.getenv("DB_PORT")
    s3_endpoint: SecretStr = os.getenv("S3_ENDPOINT")
    s3_access_key: SecretStr = os.getenv("S3_ACCESS_KEY")
    s3_secret_key: SecretStr = os.getenv("S3_SECRET_KEY")
    s3_bucket: SecretStr = os.getenv("S3_BUCKET")
    s3_region: SecretStr = os.getenv("S3_REGION")
    auth_service_url: str = os.getenv("AUTH_SERVICE_URL")

    @property
    def async_db_url(self):
        return self._get_db_url(sync=False)

    @property
    def sync_db_url(self):
        return self._get_db_url(sync=True)

    def _get_db_url(self, sync=False):
        return (
            f"postgresql{'' if sync else '+asyncpg'}://"
            f"{self.db_username.get_secret_value()}:"
            f"{self.db_password.get_secret_value()}@"
            f"{self.db_host.get_secret_value()}:"
            f"{self.db_port.get_secret_value()}/"
            f"{self.db_database.get_secret_value()}"
        )


settings = Settings()
