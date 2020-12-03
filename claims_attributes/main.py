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

router = APIRouter()

# It is necessary to use this to get the path of the current file
file_name = inspect.getframeinfo(inspect.currentframe()).filename
curr_path = os.path.dirname(os.path.abspath(file_name))

print("Initializing vectorizer...")
vectorizer = joblib.load(os.path.join(curr_path, "data/vectorizer.pkl"))

print("Initializing model...")
model = joblib.load(os.path.join(curr_path, "data/LRclf.pkl"))

print("Initializing classification codes and labels...")
classes = {}
with open(os.path.join(curr_path, "data/classification_text.csv"), mode="r") as infile:
    dict_reader = csv.DictReader(infile)
    classes = {i["label"].lower().strip(): i["id"] for i in dict_reader}
print("codes and labels loaded")


def predict(
    input_text: List[str] = ["Hello world"],
    vectorizer: CountVectorizer = None,
    model: LogisticRegression = None,  # TO-DO: replace model
    classes: List[str] = [],
    *args,
    **kwargs,
):
    assert vectorizer is not None
    assert model is not None
    vectored_text = csr_matrix(vectorizer.transform(input_text).toarray().tolist())
    predictions = model.predict(vectored_text)
    confidence = str(int(model.predict_proba(vectored_text).max() * 100))
    contentions = []
    for i, prediction in enumerate(predictions):
        prediction = prediction.lower().strip()
        classification = Classification(
            text=prediction, code=classes[prediction], confidence=confidence
        )
        flashes = get_flashes(input_text[i])
        special_issues = get_special_issues(input_text[i])

        contention = Contention(
            originalText=input_text[i],
            classification=classification,
            flashes=flashes,
            specialIssues=special_issues,
        )
        contentions.append(contention)
    return contentions


@router.get("/healthcheck", status_code=200)
async def healthcheck():
    return "App OK"


@router.post(f"/", response_model=Prediction)
def claims_attributes_API(claim_input: ClaimInput):
    """
    This takes an array of user's claimed disabilities (`claims_text`) and outputs a VA classification code and set of special attributes (`special issues` and `flashes`) for each.
    """
    contentions = predict(
        input_text=claim_input.claim_text,
        vectorizer=vectorizer,
        model=model,
        classes=classes,
    )
    prediction = Prediction(contentions=contentions)
    return prediction


app.include_router(router, prefix=f"/{api_prefix}/{version}")
