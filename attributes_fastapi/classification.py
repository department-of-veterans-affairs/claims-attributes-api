from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from sklearn.externals.joblib import load as pickle_loader
from scipy.sparse.csr import csr_matrix
from .schemas import (
    ClaimInput, Classification, Contention, Prediction
)
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from typing import List
import os
import csv


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Claims Attributes API",
        version="1.0.0",
        description="""
                    The Claims Attributes API...
                    """,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


print("Initializing vectorizer...")
app = FastAPI()
app.openapi = custom_openapi
vectorizer = pickle_loader(os.path.join(
    os.getcwd(), "attributes_fastapi/data/vectorizer.pkl"))

print("Initializing model...")
model = pickle_loader(os.path.join(
    os.getcwd(), "attributes_fastapi/data/LRclf.pkl"))

classes = {}
# Load classification codes and labels
with open(os.path.join(
        os.getcwd(), "attributes_fastapi/data/classification_text.csv"),
        mode='r') as infile:
    dict_reader = csv.DictReader(infile)
    classes = {i['label'].lower().strip(): i['id'] for i in dict_reader}
print('codes and labels loaded')

# vectorizer = model = classes = None


def predict(input_text: List[str] = ['Hello world'],
            vectorizer: CountVectorizer = None,
            model: LogisticRegression = None,  # TO-DO: replace model
            classes: List[str] = [],
            *args,
            **kwargs):
    assert(vectorizer is not None)
    assert(model is not None)
    vectored_text = csr_matrix(
        vectorizer.transform(input_text).toarray().tolist())
    predictions = model.predict(vectored_text)
    confidence = str(int(model.predict_proba(vectored_text).max()*100))
    contentions = []
    for i, prediction in enumerate(predictions):
        classification = Classification(text=prediction,
                                        code=classes[prediction],
                                        confidence=confidence)
        contention = Contention(originalText=input_text[i],
                                classification=classification,
                                flashes=[],
                                specialIssues=[])
        contentions.append(contention)
    return contentions


@ app.post("/", response_model=Prediction)
def claims_attributes_API(claim_input: ClaimInput):
    """
    Make a prediction

    This takes a user's array of claims_text inputs and outputs
    a classification code for each.
    """
    contentions = predict(input_text=claim_input.claim_text,
                          vectorizer=vectorizer,
                          model=model,
                          classes=classes)
    prediction = Prediction(contentions=contentions,
                            flashes=[],
                            specialIssues=[])
    return prediction
