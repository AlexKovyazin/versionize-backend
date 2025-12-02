from contextlib import asynccontextmanager

import uvicorn
from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka, FastapiProvider
from fastapi import FastAPI

from reviewer.src.config.settings import settings
from reviewer.src.entrypoints.router import router
from reviewer.src.middleware import logging_middleware
from reviewer.src.provider import DependencyProvider


@asynccontextmanager
async def lifespan(application: FastAPI):
    yield
    await application.state.dishka_container.close()


def get_read_app():
    app = FastAPI(
        title="Reviewer",
        version="0.0.1",
        lifespan=lifespan
    )
    app.include_router(router)
    app.middleware("http")(logging_middleware)

    container = make_async_container(
        DependencyProvider(),
        FastapiProvider()
    )
    setup_dishka(container=container, app=app)

    if settings.debug:
        app.swagger_ui_init_oauth = {
            "clientId": settings.kc_client_id,
            "clientSecret": settings.kc_client_secret.get_secret_value(),
            "scopeSeparator": " ",
            "scopes": "openid profile email",
        }

    return app


def run_read_app():
    uvicorn.run(
        'reviewer.src.read_app:get_read_app',
        factory=True,
        host="0.0.0.0",
        port=settings.read_service_port,
        reload=True if settings.debug else False,
        reload_dirs=["/usr/src"]
    )


if __name__ == '__main__':
    read_app = get_read_app()
