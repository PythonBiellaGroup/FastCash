import os
import secrets
from datetime import date
from datetime import datetime
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

# security aspects
SECURITY_ALGORITHM: str = os.environ.get("SECURITY_ALGORITHM", "HS256")
SECURITY_SECRET_KEY: str = os.environ.get(
    "SECURITY_SECRET_KEY", secrets.token_urlsafe(32)
)
SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
    os.environ.get("SECURITY_ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24 * 8)
)

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

# DEFAULT ADMIN START USER
APP_USER_USERNAME: str = os.getenv("APP_USER_USERNAME", "pbg")
APP_USER_PASSWORD: str = os.getenv("APP_USER_PASSWORD", "superDuber456!!")
APP_USER_NAME: str = os.getenv("APP_USER_NAME", "PythonBiellaGroup")
APP_USER_SURNAME: str = os.getenv("APP_USER_SURNAME", "PythonBiellaGroup")
APP_USER_EMAIL: str = os.getenv("APP_USER_EMAIL", "pythonbiellagroup@gmail.com")
APP_USER_BIRTH_DATE: date = datetime.strptime(
    os.getenv("APP_USER_BIRTH_DATE", "2021-10-11"), "%Y-%m-%d"
).date()
APP_USER_ISADMIN: bool = bool(os.getenv("APP_USER_ISADMIN", "True"))

# Read the configurations
# APP_CONFIG = read_yaml(config_path, filename="settings.yml")

# logger.info(f"App path: {APP_PATH}")
# logger.info(f"Config path: {config_path}")
# logger.info(f"Get folder path: {get_folder_path}")
