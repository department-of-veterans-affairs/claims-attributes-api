from fastapi import FastAPI, APIRouter
from .routers import docs, healthcheck, predict

# All API calls have this prefix in order to avoid Load Balancer conflicts
api_prefix = "benefits-claims-attributes"
version = "v1"

app = FastAPI(
    docs_url=f"/{api_prefix}/{version}/docs",
    openapi_url=f"/{api_prefix}/{version}/docs/openapi.json"
)

app.include_router(router, prefix=f"/{api_prefix}/{version}")
global_router = APIRouter()
global_router.include_router(docs.router)
global_router.include_router(healthcheck.router)
global_router.include_router(predict.router)
