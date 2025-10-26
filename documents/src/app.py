from fastapi import FastAPI

from src.config.settings import settings
from src.entrypoints.router import router
from src.middleware import logging_middleware

app = FastAPI(
    title="Documents",
    version="0.0.1",
)
app.include_router(router)
app.middleware("http")(logging_middleware)

if settings.debug:
    app.swagger_ui_init_oauth = {
        "clientId": settings.kc_client_id,
        "clientSecret": settings.kc_client_secret.get_secret_value(),
        "scopeSeparator": " ",
        "scopes": "openid profile email",
    }
