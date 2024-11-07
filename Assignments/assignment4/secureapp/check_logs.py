import logging
from datetime import datetime
import os

# Configure logger
logger = logging.getLogger('django')

# Log file path
LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), 'suspicious_activity.log')
LAST_PROCESSED_LINE_FILE = os.path.join(os.path.dirname(__file__), 'last_processed_line.txt')

def get_last_processed_line():
    """Retrieve the last processed line number from a file."""
    try:
        with open(LAST_PROCESSED_LINE_FILE, 'r') as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0

def set_last_processed_line(line_number):
    """Store the last processed line number."""
    with open(LAST_PROCESSED_LINE_FILE, 'w') as f:
        f.write(str(line_number))

def check_logs():
    # Retrieve last processed line to avoid re-checking old entries
    last_processed_line = get_last_processed_line()
    current_line = 0

    # Open the log file
    with open(LOG_FILE_PATH, 'r') as file:
        for line in file:
            current_line += 1
            # Only check lines that haven’t been processed
            if current_line > last_processed_line:
                if 'Suspicious Activity' in line:
                    # Perform an action, e.g., send an email alert
                    logger.warning(f"ALERT: Found suspicious activity in the logs at {datetime.now()}")

    # Update the last processed line
    set_last_processed_line(current_line)

if __name__ == "__main__":
    check_logs()
