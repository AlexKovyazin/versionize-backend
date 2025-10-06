from fastapi import FastAPI

from identity.src.entrypoints.router import router
from identity.src.middleware import logging_middleware

app = FastAPI(
    title="Identity",
    version="0.0.1",
)
app.include_router(router)
app.middleware("http")(logging_middleware)
