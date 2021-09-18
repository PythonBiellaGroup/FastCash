from fastapi import FastAPI
import uvicorn
from starlette.middleware.cors import CORSMiddleware

from app.src.api.api_v1.api import api_router
from app.src.config import (
    API_ENDPOINT_HOST,
    API_ENDPOINT_PORT,
    DEBUG_MODE,
    PROJECT_NAME,
    API_V1_STR,
    BACKEND_CORS_ORIGINS,
)

app = FastAPI(title=PROJECT_NAME, openapi_url=f"{API_V1_STR}/openapi.json")

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


if __name__ == "__main__":

    if DEBUG_MODE:
        uvicorn.run(app, port=API_ENDPOINT_PORT, host=API_ENDPOINT_HOST)
