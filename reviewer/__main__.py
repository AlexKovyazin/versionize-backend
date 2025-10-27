import uvicorn

from reviewer.src.config.settings import settings

uvicorn.run(
    'reviewer.src.app:app',
    host="0.0.0.0",
    port=settings.service_port,
    reload=True if settings.debug else False,
)
