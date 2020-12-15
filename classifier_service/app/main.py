import csv
from pathlib import Path
from typing import List, Dict

import joblib
import requests
from fastapi import FastAPI
from importlib_resources import files
from scipy.sparse.csr import csr_matrix
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression

from .schemas import Classification, ClaimInput

app = FastAPI()
classifier = None


@app.on_event("startup")
def startup_event():
    print("Initializing vectorizer...")
    vectorizer_path = files("app.data").joinpath("vectorizer.pkl")
    vectorizer = joblib.load(vectorizer_path)

    print("Initializing model...")
    model_path = files("app.data").joinpath("LRclf.pkl")
    model = joblib.load(model_path)

    print("Initializing classification codes and labels...")
    classifier_codes = files("app.data").joinpath("classification_text.csv")
    classes = {}
    with classifier_codes.open("r") as infile:
        dict_reader = csv.DictReader(infile)
        for classification in dict_reader:
            label = classification["label"].lower().strip()
            classes[label] = classification["id"]
    print("codes and labels loaded")
    global classifier
    classifier = DisabilityClassifier(model, vectorizer, classes)


class DisabilityClassifier:
    def __init__(
        self,
        model: LogisticRegression,
        vectorizer: CountVectorizer,
        classes: Dict[str, int],
    ):
        self.model = model
        self.vectorizer = vectorizer
        self.classes = classes

    def classify(self, text):
        vectorized_text = csr_matrix(
            self.vectorizer.transform([text]).toarray().tolist()
        )
        prediction = self.model.predict(vectorized_text)[0].lower().strip()
        confidence = round(self.model.predict_proba(vectorized_text).max(), 2)
        classification = Classification(
            text=prediction, code=self.classes[prediction], confidence=confidence
        )
        return classification


@app.post("/", response_model=List[Classification])
async def classify(claim_input: ClaimInput):
    return [classifier.classify(text) for text in claim_input.claim_text]
