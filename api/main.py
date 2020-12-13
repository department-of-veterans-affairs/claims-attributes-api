from fastapi import FastAPI, APIRouter
from .routers import healthcheck, predict

# All API calls have this prefix in order to avoid Load Balancer conflicts
api_prefix = "benefits-claims-attributes"
version = "v1"

app = FastAPI(
    docs_url=f"/{api_prefix}/{version}/docs",
    openapi_url=f"/{api_prefix}/{version}/docs/openapi.json"
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Claims Attributes API",
        version="1.0.0",
        description=Path("claims_attributes/summary.md").read_text(),
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema

global_router = APIRouter()
global_router.include_router(healthcheck.router)
global_router.include_router(predict.router)
global_router.openapi = custom_openapi
app.include_router(global_router, prefix=f"/{api_prefix}/{version}")