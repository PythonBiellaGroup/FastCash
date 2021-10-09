from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.src.db.manager import create_table
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


async def api_token(token: str = Depends(APIKeyHeader(name="Token"))):
    if token != APP_API_TOKEN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)


app = FastAPI(title=PROJECT_NAME,
              openapi_url=f"{API_V1_STR}/openapi.json",
              dependencies=[Depends(api_token)])

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
async def on_startup():
    await create_table()


if __name__ == "__main__":
    logger.debug(f"Starting server on: {API_ENDPOINT_HOST}:{API_ENDPOINT_PORT}")
    uvicorn.run(app, port=API_ENDPOINT_PORT, host=API_ENDPOINT_HOST, reload=DEBUG_MODE)
