import sys
import logging
from recipe_bot.logger import logger  # import your custom logger

# Function to get detailed error information (filename, line number, and message)
def error_message_detail(error, error_detail: sys):
    """
    Returns a detailed string with filename, line number, and error message.
    """
    _, _, exc_tb = error_detail.exc_info()  # extract traceback info
    file_name = exc_tb.tb_frame.f_code.co_filename  # which file caused it
    line_number = exc_tb.tb_lineno  # which line caused it
    error_message = f"Error occurred in script [{file_name}] at line [{line_number}]: {str(error)}"
    return error_message


# Custom exception class for the project
class CustomException(Exception):
    """
    A custom exception class that captures and logs detailed error messages.
    """
    def __init__(self, error_message, error_detail: sys):
        # Generate a detailed message
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        # When you print the error, it shows the full detail
        return self.error_message


# Example usage (remove this part in production)
if __name__ == "__main__":
    try:
        x = 10 / 0  # This will raise a ZeroDivisionError
    except Exception as e:
        raise CustomException(e, sys)