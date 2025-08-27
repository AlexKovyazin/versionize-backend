from fastapi import FastAPI

from documents.src.entrypoints.router import router

app = FastAPI(
    title="Documents",
    version="0.0.1",
)
app.include_router(router)
