import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logging(logs_directory="logs"):
    """Set up logging configuration and avoid adding duplicate handlers."""

    # Check if the logger has handlers already (to avoid duplicates)
    if len(logging.getLogger().handlers) > 0:
        return  # Logging has already been set up, no need to do it again

    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    log_file = datetime.now().strftime("parser_log_%Y-%m-%d_%H-%M-%S.log")
    log_path = os.path.join(logs_directory, log_file)

    # Setup log rotation: Max file size 5MB, keep 5 backup files
    handler = RotatingFileHandler(log_path, maxBytes=5*1024*1024, backupCount=5)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    # Configure the root logger
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Console logging
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    logging.info("Logging setup complete.")
