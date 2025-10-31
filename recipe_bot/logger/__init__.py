import logging
import os
from datetime import datetime

# Create a folder named "logs" (if it doesn't exist yet)
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Generate a log file name with the current date and time
log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

# Set up the basic configuration for logging
logging.basicConfig(
    level=logging.INFO,  # This means: record INFO and anything more serious (WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Defines how each log line looks
    handlers=[
        logging.FileHandler(log_file),  # Save logs to a file
        logging.StreamHandler()         # Also show logs in the console
    ]
)

# Create a logger object (you can import this in any file)
logger = logging.getLogger("CookingAssistant")

# Example usage: these lines will show how it works
if __name__ == "__main__":
    logger.info("Logger started successfully!")
    logger.warning("This is a test warning.")
    logger.error("Example error log.")