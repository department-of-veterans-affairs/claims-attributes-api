from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import requests
import logging
from caapi_shared.schemas import (
    ClaimInput,
    Contention,
    Prediction,
    ClassifierServiceOutput,
    SpecialIssueServiceOutput,
    FlashesServiceOutput,
)
from app.settings import settings


router = APIRouter()


class Predictor:
    async def predict(self, claim_input: ClaimInput):
        contentions = []
        classifications = self.safe_post(
            settings.classifier_uri, claim_input.json(), ClassifierServiceOutput
        ).classifications

        special_issues = self.safe_post(
            settings.special_issues_uri, claim_input.json(), SpecialIssueServiceOutput
        ).special_issues

        flashes = self.safe_post(
            settings.flashes_uri, claim_input.json(), FlashesServiceOutput
        ).flashes

        for (input_text, classification, special_issues, flashes) in zip(
            claim_input.claim_text,
            classifications,
            special_issues,
            flashes,
        ):
            contention = Contention(
                originalText=input_text,
                classification=classification,
                specialIssues=special_issues,
                flashes=flashes,
            )
            contentions.append(contention)
        return Prediction(contentions=contentions)

    def safe_post(self, url: str, data: dict, model: BaseModel):
        parsed_data = None
        response = requests.post(url, data=data)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(
                f"Abnormal response code connecting to {url}: {response.status_code}, {e}"
            )
            raise
        parsed_data = model.parse_obj(response.json())
        return parsed_data


@router.post("/", response_model=Prediction, tags=["Claims Attributes"])
async def get_prediction(claim_input: ClaimInput):
    """
    This takes an array of user's claimed disabilities (`claims_text`) and
    outputs a VA classification code and set of special attributes
    (`special issues` and `flashes`) for each.
    """
    predictor = Predictor()
    prediction = await predictor.predict(claim_input=claim_input)
    return prediction
