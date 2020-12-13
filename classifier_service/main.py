import joblib
from pathlib import Path
import csv
import typing
import caapi_shared.schemas as schemas
from fastapi import FastAPI
from sklearn.linear_model import LogisticRegression
import requests

app = FastAPI()
classifier = None

@app.on_event("startup")
def startup_event():
    print("Initializing model...")
    classifier_path = Path("data/LRclf.pkl")
    model = joblib.load(classifier_path)

    print("Initializing classification codes and labels...")
    classifier_path = Path("data/classification_text.csv")
    with classifier_path.open("r") as infile:
        dict_reader = csv.DictReader(infile)
        for classification in dict_reader:
            label = classification["label"].lower().strip()
            classes[label] = classification["id"]
    print("codes and labels loaded")
    classifier = CodeClassifier(model, classes)
    

class CodeClassifier:
    def __init__(self, model: LogisticRegression, classes:[str]):
        self.model = model
        self.classes = classes
    
    def classify(self, original_text, vectorized_text):
        prediction = self.model.predict(vectorized_text).lower().strip()
        confidence = str(int(model.predict_proba(vectorized_text).max() * 100))
        classification = Classification(
            text=prediction, code=classes[prediction], confidence=confidence
        )
        return classification

@app.post("/", response_model=List[Classification])
async def vectorize(claim_input: ClaimInput):
    original_text_array = claim_input.claim_text
    vectorized_text_array = await requests.get("vectorizer", params={claim_text: original_text_array}).json()
    classifications = []
    for (original_text, vectorized_text) in zip(original_text_array, vectorized_text_array):
        classifications.append(classifier.classify(original_text, vectorized_text))
    return classifications