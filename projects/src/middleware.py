import logging
import time
import traceback
import uuid
from typing import Callable

from fastapi import Request

from projects.src.config.logging import user_ip_var, request_id_var

logger = logging.getLogger(__name__)


async def logging_middleware(request: Request, call_next: Callable):
    # Generate request ID
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request_id_var.set(request_id)

    # Get client IP
    user_ip = request.client.host if request.client else None
    user_ip_var.set(user_ip)

    start_time = time.time()

    # Log request start
    logger.info(
        f"Request {request.url.path} started",
        extra={
            "extra_fields": {
                "request_id": request_id,
                "user_ip": user_ip,
                "method": request.method,
                "url": str(request.url),
                "user_agent": request.headers.get("user-agent"),
                "endpoint": request.url.path,
            }
        }
    )

    try:
        response = await call_next(request)
        process_time = time.time() - start_time

        # Log request completion
        logger.info(
            f"Request {request.url.path} completed",
            extra={
                "extra_fields": {
                    "request_id": request_id,
                    "user_ip": user_ip,
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time_ms": round(process_time * 1000, 2),
                    "response_size": response.headers.get("content-length", 0),
                }
            }
        )

        # Add request ID to response headers
        response.headers["X-Request-ID"] = request_id
        return response

    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            "Request failed",
            extra={
                "extra_fields": {
                    "request_id": request_id,
                    "user_ip": user_ip,
                    "method": request.method,
                    "url": str(request.url),
                    "error_type": type(e).__name__,
                    "error_message": str(e),
                    "traceback": traceback.format_exc(),
                    "process_time_ms": round(process_time * 1000, 2),
                }
            },
            exc_info=True
        )
        raise

    finally:
        # Clean up context variables
        request_id_var.set(None)
        user_ip_var.set(None)
