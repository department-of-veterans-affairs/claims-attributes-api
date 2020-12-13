import joblib
from pathlib import Path
from .schemas import VectorizerOutput
import caapi_shared.schemas as shared_schemas
from scipy.sparse.csr import csr_matrix
from fastapi import FastAPI

app = FastAPI()
vectorizer = None

@app.on_event("startup")
def startup_event():
    print("Initializing vectorizer...")
    vectorizer_path = Path("data/vectorizer.pkl")
    vectorizer = joblib.load(vectorizer_path)

@app.get("/{text}", response_model=VectorizerOutput)
def vectorize(claim_input: shared_schemas.ClaimInput):
    vectorized_text = csr_matrix(vectorizer.transform(input_text).toarray().tolist())
    return {"vectorized_text": vectorized_text}
