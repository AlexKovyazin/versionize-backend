from dishka import make_async_container
from dishka.integrations.faststream import setup_dishka, FastStreamProvider
from faststream import FastStream

from projects.src.entrypoints.router import broker
from projects.src.provider import DependencyProvider


def get_write_app():
    app = FastStream(
        broker
    )
    container = make_async_container(
        DependencyProvider(),
        FastStreamProvider()
    )
    setup_dishka(
        container=container,
        auto_inject=True,
        app=app,
    )
    return app


async def run_write_app():
    app = get_write_app()
    return await app.run()
