import fastapi
import uvicorn

from live.src.api.api import api_router
from live.src.config import API_ENDPOINT_PORT, API_ENDPOINT_HOST, PROJECT_NAME, API_STR
from live.src.db.manager import create_table

app = fastapi.FastAPI(title=PROJECT_NAME, openapi_url=f"{API_STR}/openapi.json")


app.include_router(api_router, prefix=API_STR)


@app.on_event("startup")
def on_startup():
    create_table()


@app.get("/")
def index():
    body = (
        "<html>"
        "<body style='padding: 10px;'>"
        "<h1>Ciao PythonBiellaGroup</h1>"
        "</body>"
        "</html>"
    )
    return fastapi.responses.HTMLResponse(content=body)


if __name__ == "__main__":
    uvicorn.run("main:api", port=API_ENDPOINT_PORT, host=API_ENDPOINT_HOST, reload=True)
