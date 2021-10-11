import uvicorn
from starlette.middleware.cors import CORSMiddleware
from sqlmodel import select
from fastapi import FastAPI, responses


# from app.src.api.endpoints.login import api_token
from app.src.common.security import get_password_hash
from app.src.db.engine import get_session_sqlmodel
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

app = FastAPI(
    title=PROJECT_NAME,
    openapi_url=f"{API_V1_STR}/openapi.json",
    # dependencies=[Depends(api_token)],
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
        password=get_password_hash(APP_USER_PASSWORD),
        isAdmin=APP_USER_ISADMIN,
    )

    # check if the user exist
    session = get_session_sqlmodel()
    query = select(AppUser).where(AppUser.username == admin_user.username)
    check_user = session.exec(query).first()
    if check_user:
        logger.debug("Default user not inserted, user already exist...")
    else:
        # insert the admin user
        insert_data(admin_user)
        logger.debug("Default user inserted")


@app.get("/")
def index():
    url_swagger = f"http://{API_ENDPOINT_HOST}:{API_ENDPOINT_PORT}/docs"
    url_redoc = f"http://{API_ENDPOINT_HOST}:{API_ENDPOINT_PORT}/redoc"
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Welcome to: PythonBiellaGroup FastCash Server App</h1>"
        "<ul>"
        f"<li><a href={url_swagger}>Link to the Swagger documentation</a></li>"
        f"<li><a href={url_redoc}>Link to the Redoc documentation</a></li>"
        "</ul>"
        "</body>"
        "</html>"
    )
    return responses.HTMLResponse(content=body)


if __name__ == "__main__":
    logger.info(f"Starting server on: {API_ENDPOINT_HOST}:{API_ENDPOINT_PORT}")

    if DEBUG_MODE:
        uvicorn.run(app, port=API_ENDPOINT_PORT, host=API_ENDPOINT_HOST)
