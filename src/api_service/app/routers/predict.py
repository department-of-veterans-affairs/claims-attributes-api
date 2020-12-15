from fastapi import APIRouter
from typing import List
import requests
from app.schemas import ClaimInput, Contention, Prediction
from app.settings import settings


router = APIRouter()


class Predictor:
    async def predict(self, input_text: List[str] = ["Hello world"]):
        contentions = []
        classification_list = await requests.post(
            settings.CLASSIFIER_URI, data=input_text
        )
        special_issues_list = await requests.post(
            settings.SPECIAL_ISSUES_URI, data=input_text
        )
        flashes_list = await requests.post(settings.FLASHES_URI, data=input_text)

        for (input_text, classification, special_issues, flashes) in zip(
            input_text, classification_list, special_issues_list, flashes_list
        ):
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
    This takes an array of user's claimed disabilities (`claims_text`) and
    outputs a VA classification code and set of special attributes
    (`special issues` and `flashes`) for each.
    """
    predictor = Predictor()
    prediction = await predictor.predict(input_text=claim_input.claim_text)
    return prediction
