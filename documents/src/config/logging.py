import json
import logging
import os
import sys
from logging.handlers import RotatingFileHandler


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "message": record.getMessage(),
            "service": "fastapi-app",
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add extra fields if present
        if hasattr(record, 'extra_fields'):
            log_entry.update(record.extra_fields)

        return json.dumps(log_entry)


class ContextLogger:
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def info(self, message: str, **kwargs):
        self.logger.info(message, extra={"extra_fields": kwargs})

    def error(self, message: str, **kwargs):
        self.logger.error(message, extra={"extra_fields": kwargs})

    def warning(self, message: str, **kwargs):
        self.logger.warning(message, extra={"extra_fields": kwargs})

    def debug(self, message: str, **kwargs):
        self.logger.debug(message, extra={"extra_fields": kwargs})


def setup_logging():
    # Create logs directory if it doesn't exist
    os.makedirs('/var/log', exist_ok=True)

    # Root logger configuration
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # Clear any existing handlers
    logger.handlers.clear()

    # Console handler (for development)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    console_handler.setFormatter(console_formatter)

    # File handler (for Loki via Promtail)
    file_handler = RotatingFileHandler(
        '/var/log/documents.log',
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(file_formatter)

    # JSON file handler (structured logging)
    json_file_handler = RotatingFileHandler(
        '/var/log/documents-json.log',
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
