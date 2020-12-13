from fastapi import APIRouter
from pathlib import Path
from caapi_shared.schemas import ClaimInput, Classification, Contention, Prediction
from typing import List

router = APIRouter()

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



@router.post("/", response_model=Prediction)
async def get_prediction(claim_input: ClaimInput):
    """
    This takes an array of user's claimed disabilities (`claims_text`) and outputs a VA classification code and set of special attributes (`special issues` and `flashes`) for each.
    """
    predictor = Predictor()
    prediction = predictor.predict(input_text=claim_input.claim_text)
    return prediction

