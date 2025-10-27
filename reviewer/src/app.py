from fastapi import FastAPI

from reviewer.src.config.settings import settings
from reviewer.src.entrypoints.router import router
from reviewer.src.middleware import logging_middleware

app = FastAPI(
    title="Reviewer",
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
