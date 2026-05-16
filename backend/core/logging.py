import logging
from logging.handlers import RotatingFileHandler
from backend.core.config import settings


def configure_logging() -> None:
    """Configure structured logging for the document intelligence service."""
    logger = logging.getLogger()
    logger.setLevel(settings.LOG_LEVEL)

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = RotatingFileHandler(
        "logs/service.log",
        maxBytes=5_242_880,
        backupCount=5,
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)


def get_logger(name: str):
    return logging.getLogger(name)
