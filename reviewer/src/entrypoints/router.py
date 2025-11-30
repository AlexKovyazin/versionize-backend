from fastapi import APIRouter
from faststream.nats import NatsBroker

from reviewer.src.config.settings import settings
from reviewer.src.entrypoints.remark_docs import api_router as remark_docs_api_router
from reviewer.src.entrypoints.remarks import api_router as remarks_api_router
from reviewer.src.entrypoints.remarks import broker_router as remarks_broker_router
from reviewer.src.entrypoints.service import router as service_router

router = APIRouter()
broker = NatsBroker(settings.nats_url)

router.include_router(service_router, prefix="/service")

router.include_router(remarks_api_router, prefix="/remarks")
broker.include_router(remarks_broker_router)
router.include_router(remark_docs_api_router, prefix="/remark-docs")
broker.include_router(remarks_broker_router)
