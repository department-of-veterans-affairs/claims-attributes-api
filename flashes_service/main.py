from caapi_shared.utils as utils
from caapi_shared.schemas import Flash
from fastapi import FastAPI

app = FastAPI()

class SpecialIssuesClassifier:
    def __init__(self):
        self.flashes_map = json.load(Path("flashes.json").read_text())

    def check_keywords(self, claim_text):
        flashes = []
        if "hardship" in claim_text:
            flashes.append("Hardship")
        if "seriously injured" in claim_text:
            flashes.append("Seriously Injured/Very Seriously Injured")
        if "terminally ill" in claim_text:
            flashes.append("Terminally Ill")
        if "homeless" in claim_text:
            flashes.append("Homeless")
        if "purple heart" in claim_text:
            flashes.append("Purple Heart")
        if ("pow" in x) or ("prisoner of war" in claim_text) or ("p o w" in claim_text):
            flashes.append("POW")
        if "medal of honor" in claim_text:
            flashes.append("Medal of Honor")
        if ("amyotrophic lateral sclerosis" in claim_text) or ("als" in x) or ("a l s" in x):
            flashes.append("Amyotrophic Lateral Sclerosis")
        if "emergency care" in claim_text:
            flashes.append("Emergency Care")
        return flashes

    def classify(self, claim_text):
        cleaned_text = utils.clean_text(text)
        keyword_matches = self.check_keywords(cleaned_text)
        spelling_matches = utils.find_similar(cleaned_text, self.flashes_map)
        matches = keyword_matches + spelling_matches
        match_results = []
        for match in matches:
            match_results.append({
                "text": match
            })
        return match_results

@app.get("/")
def get_flashes(claim_input: ClaimInput) -> [Flash]:
    classifier = FlashesClassifier()
    flash_list = []
    for claim_text in claim_input.claim_text:
        flash_list.append(classifier.classify(claim_text))
    return flash_list

