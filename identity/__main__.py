import uvicorn

from identity.src.config.settings import settings

uvicorn.run(
    'identity.src.app:app',
    host="0.0.0.0",
    port=settings.service_port,
    reload=True if settings.debug else False,
)
