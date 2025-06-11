import logging
import sys
from typing import Optional


def setup_logging(
    level: int = logging.INFO,
    log_file: Optional[str] = None,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
) -> None:
    """
    Set up logging configuration for the application.

    Args:
        level: Logging level (default: INFO)
        log_file: Optional path to log file. If not provided, logs will go to stdout
        log_format: Format string for log messages
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove any existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatter
    formatter = logging.Formatter(log_format)

    # Create and configure console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # If log file is specified, add file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)

    # Set logging level for specific loggers
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.WARNING)
