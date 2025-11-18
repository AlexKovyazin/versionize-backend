from contextlib import asynccontextmanager

from fastapi import FastAPI

from bff.src.adapters.nats.nats import NatsJS
from bff.src.config.settings import settings
from bff.src.entrypoints.router import router
from bff.src.middleware import logging_middleware


@asynccontextmanager
async def lifespan(application: FastAPI):
    nats_adapter = NatsJS()
    await nats_adapter.connect()

    yield

    await nats_adapter.disconnect()


app = FastAPI(
    title="Backend For Fronted",
    version="0.0.1",
    lifespan=lifespan,
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
