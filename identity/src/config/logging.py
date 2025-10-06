import datetime
import json
import logging
import os
import sys
from contextvars import ContextVar
from decimal import Decimal
from enum import Enum
from logging.handlers import RotatingFileHandler
from typing import Optional, Any

request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_ip_var: ContextVar[Optional[str]] = ContextVar('user_ip', default=None)


class ContextFilter(logging.Filter):
    def filter(self, record):
        record.request_id = request_id_var.get()
        record.user_ip = user_ip_var.get()
        return True


class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        try:
            return str(obj)
        except Exception:
            return super().default(obj)


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": "identity",
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
            "request_id": getattr(record, 'request_id', None),
            "user_ip": getattr(record, 'user_ip', None),
        }

        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)

        return json.dumps(log_entry, cls=CustomJSONEncoder, ensure_ascii=False)


class ContextLogger:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    @staticmethod
    def _get_context(**kwargs) -> dict[str, Any]:
        """Get current context and merge with provided kwargs."""
        context = {
            "request_id": request_id_var.get(),
            "user_ip": user_ip_var.get(),
        }
        context.update(kwargs)
        return {k: v for k, v in context.items() if v is not None}

    def info(self, message: str, **kwargs):
        context = self._get_context(**kwargs)
        self.logger.info(message, extra={"extra_fields": context}, stacklevel=3)

    def error(self, message: str, **kwargs):
        context = self._get_context(**kwargs)
        self.logger.error(message, extra={"extra_fields": context}, stacklevel=3, exc_info=True)

    def warning(self, message: str, **kwargs):
        context = self._get_context(**kwargs)
        self.logger.warning(message, extra={"extra_fields": context}, stacklevel=3)

    def debug(self, message: str, **kwargs):
        context = self._get_context(**kwargs)
        self.logger.debug(message, extra={"extra_fields": context}, stacklevel=3)


def setup_logging():
    # Create logs directory if it doesn't exist
    os.makedirs('/var/log', exist_ok=True)

    # Root logger configuration
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear any existing handlers
    logger.handlers.clear()

    # Add context filter
    context_filter = ContextFilter()
    logger.addFilter(context_filter)

    # Console handler (for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(request_id)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)
    console_handler.addFilter(context_filter)

    # File handler (for Loki via Promtail)
    file_handler = RotatingFileHandler(
        '/var/log/identity.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(request_id)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.addFilter(context_filter)

    # JSON file handler (structured logging)
    json_file_handler = RotatingFileHandler(
        '/var/log/identity-json.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    json_file_handler.setLevel(logging.INFO)
    json_formatter = JSONFormatter()
    json_file_handler.setFormatter(json_formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    logger.addHandler(json_file_handler)

    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)


setup_logging()
logger = ContextLogger(logging.getLogger(__name__))
