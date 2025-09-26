from fastapi import FastAPI

from documents.src.entrypoints.router import router
from documents.src.middleware import logging_middleware

app = FastAPI(
    title="Documents",
    version="0.0.1",
)
app.include_router(router)
app.middleware("http")(logging_middleware)
