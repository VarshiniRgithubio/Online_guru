"""
Logging configuration for the Sai Baba Guidance Chatbot.
Centralizes logging setup using loguru.
"""

import sys
from pathlib import Path
from loguru import logger

from config import settings


def setup_logging():
    """
    Configure logging for the application.
    Sets up both console and file logging with appropriate formatting.
    """
    # Remove default handler
    logger.remove()
    
    # Console handler with color
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.log_level,
        colorize=True
    )
    
    # File handler
    log_path = Path(settings.log_file)
    logger.add(
        str(log_path),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.log_level,
        rotation="10 MB",  # Rotate when file reaches 10 MB
        retention="30 days",  # Keep logs for 30 days
        compression="zip",  # Compress rotated logs
        enqueue=True  # Thread-safe logging
    )
    
    logger.info("Logging configured successfully")


# Setup logging when module is imported
setup_logging()
