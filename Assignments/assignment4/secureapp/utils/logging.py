# utils/logging.py

import logging

# Create a custom logger
logger = logging.getLogger('django')

def log_suspicious_activity(message):
    # Log suspicious activity at WARNING level
    logger.warning(f"Suspicious Activity: {message}")
