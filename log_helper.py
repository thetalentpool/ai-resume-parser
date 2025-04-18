import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler
import uuid  # Added import

def setup_logging(logs_directory="logs"):
    """Set up logging configuration with a unique log file per process/thread."""

    # Check if the logger has handlers already (to avoid duplicates)
    if len(logging.getLogger().handlers) > 0:
        return  # Logging is already set up

    if not os.path.exists(logs_directory):
        os.makedirs(logs_directory)

    # Create a unique log file name using uuid
    short_id = uuid.uuid4().hex[:5]
    log_file = f"parser_log_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S-%f')}_{short_id}.log"
    log_path = os.path.join(logs_directory, log_file)

    # Setup log rotation
    handler = RotatingFileHandler(log_path, maxBytes=5 * 1024 * 1024, backupCount=5)
    handler.setLevel(logging.INFO)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    # Also log to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(console_handler)

    logging.info("Logging setup complete.")
