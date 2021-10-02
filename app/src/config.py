import os

from typing import List
from pydantic import AnyHttpUrl

# from app.src.common.utils import read_yaml, get_folder_path
# from app.src.logger import logger


# Set the application variables
API_ENDPOINT_PORT: int = int(os.environ.get("API_ENDPOINT_PORT", 8042))
API_ENDPOINT_HOST: str = os.environ.get("API_ENDPOINT_HOST", "127.0.0.1")
APP_SECRET_KEY: str = os.environ.get("APP_SECRET_KEY", "DEVtest42!!")
APP_API_TOKEN: str = os.environ.get("APP_API_TOKEN", "PythonBiellaGroup")
API_V1_STR: str = os.environ.get("API_V1_STR", "/api/v1")
PROJECT_NAME: str = "fastcash"
BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []


# if you want to test gunicorn the below environment variabile must be False
DEBUG_MODE: str = os.environ.get("DEBUG_MODE", "False")
VERBOSITY: str = os.environ.get("VERBOSITY", "DEBUG")

# Database settings
DB_CONFIG = {
    "db_name": os.getenv("DB_NAME", "fastcash"),
    "db_user": os.getenv("DB_USER", "root"),
    "db_password": os.getenv("DB_PASSWORD", "SUPERduper42"),
    "db_port": os.getenv("DB_PORT", "5442"),
    "db_host": os.getenv("DB_HOST", "localhost"),
}

# Application Path
APP_PATH: str = os.environ.get("PROJECT_WORKSPACE", os.path.abspath("."))

# Applications configurations
# Read the application configuration settings
config_path: str = os.path.join(APP_PATH, "app", "config")

# Read the configurations
# APP_CONFIG = read_yaml(config_path, filename="settings.yml")


# logger.info(f"App path: {APP_PATH}")
# logger.info(f"Config path: {config_path}")
# logger.info(f"Get folder path: {get_folder_path}")
