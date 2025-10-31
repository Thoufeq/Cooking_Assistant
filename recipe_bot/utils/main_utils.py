import os
import sys
import yaml
import dill
import numpy as np
from recipe_bot.logger import logger
from recipe_bot.exception import CustomException


def read_yaml(file_path: str) -> dict:
    """Read YAML configuration file."""
    try:
        with open(file_path, "r") as f:
            data = yaml.safe_load(f)
        logger.info(f"Loaded YAML from {file_path}")
        return data
    except Exception as e:
        raise CustomException(e, sys)


def save_object(file_path: str, obj: object):
    """Serialize and save a Python object."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            dill.dump(obj, f)
        logger.info(f"Object saved at {file_path}")
    except Exception as e:
        raise CustomException(e, sys)


def load_object(file_path: str):
    """Load a serialized Python object."""
    try:
        with open(file_path, "rb") as f:
            obj = dill.load(f)
        logger.info(f"Loaded object from {file_path}")
        return obj
    except Exception as e:
        raise CustomException(e, sys)


def save_numpy_array(file_path: str, array: np.ndarray):
    """Save numpy array to file."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as f:
            np.save(f, array)
    except Exception as e:
        raise CustomException(e, sys)


def load_numpy_array(file_path: str):
    """Load numpy array from file."""
    try:
        with open(file_path, "rb") as f:
            return np.load(f)
    except Exception as e:
        raise CustomException(e, sys)