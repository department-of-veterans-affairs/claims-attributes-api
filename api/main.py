from fastapi import FastAPI, APIRouter
from fastapi.openapi.utils import get_openapi
from scipy.sparse.csr import csr_matrix
from .schemas import ClaimInput, Classification, Contention, Prediction
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from typing import List
import os
import csv
import inspect
import joblib
from .flashes import get_flashes
from .special_issues import get_special_issues
from pathlib import Path

# All API calls have this prefix in order to avoid Load Balancer conflicts
api_prefix = "benefits-claims-attributes"
version = "v1"
router = APIRouter()
# We prefix all endpoints with the api prefix and version
app.include_router(router, prefix=f"/{api_prefix}/{version}")


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


app = FastAPI(
    docs_url=f"/{api_prefix}/{version}/docs",
    openapi_url=f"/{api_prefix}/{version}/docs/openapi.json",
)
app.openapi = custom_openapi

class Predictor:
    async def predict(self, input_text: List[str] = ["Hello world"]):
        contentions = []
        classified_text = await requests.post("classifier", data=input_text)
        special_issues = await requests.post("special_issues", data=input_text)
        flashes = await requests.post("flashes", data=input_text)
        
        for (input_text, classified, special_issues, flashes) in zip(input_text, classification, special_issues, flashes):
            contention = Contention(
                originalText=input_text,
                classification=classification,
                specialIssues=special_issues,
                flashes=flashes,
            )
            contentions.append(contention)
        return Prediction(contentions=contentions)

@router.get("/healthcheck", status_code=200)
async def healthcheck():
    return "App OK"

@router.post("/", response_model=Prediction)
async def get_prediction(claim_input: ClaimInput):
    """
    This takes an array of user's claimed disabilities (`claims_text`) and outputs a VA classification code and set of special attributes (`special issues` and `flashes`) for each.
    """
    predictor = Predictor()
    prediction = predictor.predict(input_text=claim_input.claim_text)
    return prediction