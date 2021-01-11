import json
from pathlib import Path
from typing import List, Set

from fastapi import FastAPI
from importlib_resources import files

from caapi_shared import utils
from caapi_shared.schemas import Flash, ClaimInput, FlashesServiceOutput

app = FastAPI()


class FlashesClassifier:
    def __init__(self):
        flashes_path = Path(files("app.data").joinpath("flashes.json"))
        self.flashes_map = json.loads(flashes_path.read_text())

    def check_keywords(self, claim_text: str) -> Set[str]:
        flashes = set()
        if "hardship" in claim_text:
            flashes.add("Hardship")
        if "seriously injured" in claim_text:
            flashes.add("Seriously Injured/Very Seriously Injured")
        if "terminally ill" in claim_text:
            flashes.add("Terminally Ill")
        if "homeless" in claim_text:
            flashes.add("Homeless")
        if "purple heart" in claim_text:
            flashes.add("Purple Heart")
        if (
            ("pow" in claim_text)
            or ("prisoner of war" in claim_text)
            or ("p o w" in claim_text)
        ):
            flashes.add("POW")
        if "medal of honor" in claim_text:
            flashes.add("Medal of Honor")
        if (
            ("amyotrophic lateral sclerosis" in claim_text)
            or ("als" in claim_text)
            or ("a l s" in claim_text)
        ):
            flashes.add("Amyotrophic Lateral Sclerosis")
        if "emergency care" in claim_text:
            flashes.add("Emergency Care")
        return flashes

    def classify(self, text: str) -> List[Flash]:
        cleaned_text = utils.clean_text(text)
        keyword_matches = self.check_keywords(cleaned_text)
        spelling_matches = utils.find_similar(cleaned_text, self.flashes_map)
        matches = list(keyword_matches.union(set(spelling_matches)))
        match_results = []
        for match in matches:
            if match:
                match_results.append(Flash(text=match))
        return match_results


@app.post("/", response_model=FlashesServiceOutput)
def get_flashes(claim_input: ClaimInput):
    classifier = FlashesClassifier()
    flashes_list = [
        classifier.classify(claim_text) for claim_text in claim_input.claim_text
    ]
    return FlashesServiceOutput(flashes=flashes_list)
