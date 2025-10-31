from recipe_bot.logger import logger
from recipe_bot.exception import CustomException
import sys

# Example: for keyword generation or query rephrasing
def generate_keywords(prompt: str, llm_model) -> str:
    """Ask an LLM to generate relevant keywords from user query."""
    try:
        response = llm_model.generate(f"Extract 3-5 keywords from this query: {prompt}")
        keywords = response.strip().split(",")
        logger.info(f"Generated keywords: {keywords}")
        return [kw.strip() for kw in keywords]
    except Exception as e:
        raise CustomException(e, sys)


# Example: response generation
def generate_response(prompt: str, llm_model) -> str:
    """Generate an assistant response from an LLM."""
    try:
        response = llm_model.generate(prompt)
        logger.info("Generated response from LLM.")
        return response
    except Exception as e:
        raise CustomException(e, sys)