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

    nats_url: str = os.getenv("NATS_URL")
    projects_read_service_url: str = os.getenv("PROJECTS_READ_SERVICE_URL")
    projects_write_service_url: str = os.getenv("PROJECTS_WRITE_SERVICE_URL")

    # full path to the /get-user endpoint of identity service
    auth_service_url: str = os.getenv("AUTH_SERVICE_URL")
    # keycloak setting are needed only in debug mode for auth with swagger
    kc_external_base_url: str = os.getenv("KC_EXTERNAL_BASE_URL")
    kc_realm: str = os.getenv("KC_REALM")
    kc_client_id: str = os.getenv("KC_CLIENT_ID")
    kc_client_secret: SecretStr = os.getenv("KC_CLIENT_SECRET")

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
