from fastapi import FastAPI, APIRouter
from fastapi.openapi.utils import get_openapi
from app.routers import healthcheck, predict
from pathlib import Path
from importlib_resources import files

# All API calls have this prefix in order to avoid Load Balancer conflicts
api_prefix = "benefits-claims-attributes"
version = "v1"

app = FastAPI(
    docs_url=f"/{api_prefix}/{version}/docs",
    openapi_url=f"/{api_prefix}/{version}/docs/openapi.json",
)


def custom_openapi():
    openapi_schema = get_openapi(
        title="Claims Attributes API",
        version="1.0.0",
        description=Path(files("app.data").joinpath("summary.md")).read_text(),
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


global_router = APIRouter()
global_router.include_router(healthcheck.router)
global_router.include_router(predict.router)
global_router.openapi = custom_openapi()
app.include_router(global_router, prefix=f"/{api_prefix}/{version}")
