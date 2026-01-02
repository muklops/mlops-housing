import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

# Create logs directory
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# Log file name with timestamp (date-wise)
LOG_FILE = f"log_{datetime.now().strftime('%Y_%m_%d')}.log"
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Logger name
LOGGER_NAME = "mlops_logger"

def get_logger():
    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.INFO)

    # Avoid duplicate logs
    if logger.handlers:
        return logger

    # Log format
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(message)s"
    )

    # File handler (rotates at 5MB, keeps 5 backups)
    file_handler = RotatingFileHandler(
        LOG_FILE_PATH,
        maxBytes=5 * 1024 * 1024,
        backupCount=5
    )
    file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


# Global logger instance
logger = get_logger()
