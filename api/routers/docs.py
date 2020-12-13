from fastapi import APIRouter
from pathlib import Path
from fastapi.openapi.utils import get_openapi

router = APIRouter()

@router.get("/docs")
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

router.openapi = custom_openapi