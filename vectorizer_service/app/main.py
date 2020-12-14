import joblib
from .schemas import VectorizerOutput
from scipy.sparse.csr import csr_matrix
from fastapi import FastAPI
from importlib_resources import files
from typing import List

app = FastAPI()
vectorizer = None


@app.on_event("startup")
def startup_event():
    print("Initializing vectorizer...")
    vectorizer_path = files("app.data").joinpath("vectorizer.pkl")
    global vectorizer
    vectorizer = joblib.load(vectorizer_path)


@app.post("/", response_model=VectorizerOutput)
def vectorize(text: List[str]):
    vectorized_text = vectorizer.transform(text).toarray().tolist()
    return {"vectorized_text": vectorized_text}
