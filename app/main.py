from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.src.db.manager import create_table, insert_data
from app.src.api.api import api_router
from app.src.logger import logger
from app.src.config import (
    API_ENDPOINT_HOST,
    API_ENDPOINT_PORT,
    DEBUG_MODE,
    PROJECT_NAME,
    API_V1_STR,
    BACKEND_CORS_ORIGINS,
    APP_API_TOKEN,
)
from app.src.config import (
    APP_USER_NAME,
    APP_USER_SURNAME,
    APP_USER_BIRTH_DATE,
    APP_USER_EMAIL,
    APP_USER_USERNAME,
    APP_USER_PASSWORD,
    APP_USER_ISADMIN,
)
from app.src.models.app_user import AppUser


async def api_token(token: str = Depends(APIKeyHeader(name="Token"))):
    if token != APP_API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


app = FastAPI(
    title=PROJECT_NAME,
    openapi_url=f"{API_V1_STR}/openapi.json",
    dependencies=[Depends(api_token)],
)

# Set all CORS enabled origins
if BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=API_V1_STR)


@app.on_event("startup")
def on_startup():
    create_table()

    # insert the admin user
    admin_user = AppUser(
        name=APP_USER_NAME,
        surname=APP_USER_SURNAME,
        birth_date=APP_USER_BIRTH_DATE,
        username=APP_USER_USERNAME,
        email=APP_USER_EMAIL,
        password=APP_USER_PASSWORD,
        isAdmin=APP_USER_ISADMIN,
    )

    # create data
    insert_data(admin_user)


if __name__ == "__main__":
    logger.debug(f"Starting server on: {API_ENDPOINT_HOST}:{API_ENDPOINT_PORT}")

    if DEBUG_MODE:
        uvicorn.run(app, port=API_ENDPOINT_PORT, host=API_ENDPOINT_HOST)
