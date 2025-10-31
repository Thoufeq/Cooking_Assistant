from recipe_bot.logger import logger
from recipe_bot.exception import CustomException
import sys

b=0

if b == 1:
    logger.info("Starting data upload process...")
logger.error("Failed to connect to MongoDB.")


try:
    a = 2/b  # This will raise a ZeroDivisionError
except Exception as e:
    raise CustomException(e, sys)
