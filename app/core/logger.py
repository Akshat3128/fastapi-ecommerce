# app/core/logger.py
import logging
from logging.handlers import RotatingFileHandler

# Create logger
logger = logging.getLogger("ecommerce")
logger.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s")

# Stream handler (console)
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

# File handler (rotating logs)
file_handler = RotatingFileHandler("logs/app.log", maxBytes=1000000, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# Prevent duplicate log entries
logger.propagate = False
