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

    # full path to the /get-user endpoint of identity service
    auth_service_url: str = os.getenv("AUTH_SERVICE_URL")
    # keycloak setting are needed only in debug mode for auth with swagger
    kc_external_base_url: str = os.getenv("KC_EXTERNAL_BASE_URL")
    kc_realm: str = os.getenv("KC_REALM")
    kc_client_id: str = os.getenv("KC_CLIENT_ID")
    kc_client_secret: SecretStr = os.getenv("KC_CLIENT_SECRET")

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

    @property
    def kc_auth_url(self):
        return (
            f"{settings.kc_external_base_url}/"
            f"realms/{settings.kc_realm}/"
            f"protocol/openid-connect/auth"
        )

    @property
    def kc_token_url(self):
        return (
            f"{settings.kc_external_base_url}/"
            f"realms/{settings.kc_realm}/"
            f"protocol/openid-connect/token"
        )


settings = Settings()
