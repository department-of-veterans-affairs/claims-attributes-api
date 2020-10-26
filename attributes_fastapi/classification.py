from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from sklearn.externals.joblib import load as pickle_loader
import csv
import os
from scipy.sparse.csr import csr_matrix

print("Initializing vectorizer...")
app = FastAPI()
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


class ClaimInput(BaseModel):
    claim_text: List[str]


def predict(txt='Hello world',
                vectorizer=None,
                model=None,
                classes=[],
                *args,
                **kwargs):
    # pred
    assert(vectorizer is not None)
    assert(model is not None)
    vectored_text = csr_matrix(vectorizer.transform(txt).toarray().tolist())
    predictions = model.predict(vectored_text)
    classifications = []
    for prediction in predictions:
        classifications.append(
            {"code": classes[prediction], "text": prediction})
    return classifications


@ app.post("/")
def predict_view(claim_input: ClaimInput):
    classifications = predict(
        claim_input.claim_text, vectorizer=vectorizer, model=model, classes=classes)
    return {"query": claim_input.claim_text, "classifications": classifications}
