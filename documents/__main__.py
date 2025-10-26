import uvicorn

from documents.src.config.settings import settings

uvicorn.run(
    'documents.src.app:app',
    host="0.0.0.0",
    port=settings.service_port,
    reload=True if settings.debug else False,
)
