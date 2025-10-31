from recipe_bot.logger import logger
from recipe_bot.exception import CustomException
import sys


def search_recipes(collection, query: str):
    """Search MongoDB collection for recipes matching the query text."""
    try:
        results = list(collection.find({"$text": {"$search": query}}))
        logger.info(f"Found {len(results)} results for query '{query}'")
        return results
    except Exception as e:
        raise CustomException(e, sys)


def rank_results(results: list, top_n=5):
    """Rank and return top N recipes."""
    try:
        ranked = results[:top_n]
        logger.info(f"Returning top {top_n} recipes.")
        return ranked
    except Exception as e:
        raise CustomException(e, sys)