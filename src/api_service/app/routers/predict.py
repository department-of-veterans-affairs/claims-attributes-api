from fastapi import APIRouter
from typing import List
import requests
from caapi_shared.schemas import ClaimInput, Contention, Prediction
from app.settings import settings


router = APIRouter()


class Predictor:
    async def predict(self, claim_input: ClaimInput):
        contentions = []
        classification_list = await requests.post(
            settings.CLASSIFIER_URI, data=claim_input
        )
        special_issues_list = await requests.post(
            settings.SPECIAL_ISSUES_URI, data=claim_input
        )
        flashes_list = await requests.post(settings.FLASHES_URI, data=claim_input)

        for (input_text, classification, special_issues, flashes) in zip(
            claim_input.claim_text,
            classification_list,
            special_issues_list,
            flashes_list,
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
    prediction = await predictor.predict(claim_input=claim_input)
    return prediction
