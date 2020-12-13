import caapi_shared.utils as utils
from caapi_shared.schemas as schemas
from fastapi import FastAPI
import json
from pathlib import Path
from typing import List

app = FastAPI()

class SpecialIssuesClassifier:
    def __init__(self):
        self.si_map = json.load(Path("special_issues.json").read_text())
    
    def check_list(self, claim_text):
        identified_issues = set()
        for issue in self.si_map.keys():
            if issue in claim_text:
                identified_issues.add(self.si_map[issue])
        if ("AOOV" in issues) and ("vietnam" in x):
            identified_issues.append("AOIV")
            identified_issues.remove("AOOV")
        if ("PTSD/1" in issues) and ("non combat" in x):
            identified_issues.append("PTSD/2")
            identified_issues.remove("PTSD/1")
        return identified_issues
    
    def classify(self, claim_text):
        cleaned_text = utils.clean_text(text)
        list_matches = self.check_list(cleaned_text)
        spelling_matches = utils.find_similar(cleaned_text, self.si_map)
        matches = list_matches + spelling_matches
        match_results = []
        for match in matches:
            match_results.append({
                "text": match
            })
        return match_results

@app.get("/", response_model=List[schemas.SpecialIssue])
def get_special_issues(claim_input: schemas.ClaimInput):
    classifier = SpecialIssuesClassifier()
    issue_list = []
    for claim_text in claim_input.claim_text:
        issue_list.append(classifier.classify(claim_text))
    return issue_list
