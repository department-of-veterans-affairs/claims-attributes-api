import json
from pathlib import Path
from typing import List

from fastapi import FastAPI
from importlib_resources import files

from . import utils
from .schemas import SpecialIssue

app = FastAPI()


class SpecialIssuesClassifier:
    def __init__(self):
        special_issues_path = Path(files("app.data").joinpath("special_issues.json"))
        self.si_map = json.loads(special_issues_path.read_text())

    def check_list(self, claim_text: str):
        identified_issues = set()
        for issue in self.si_map.keys():
            if issue in claim_text:
                identified_issues.add(self.si_map[issue])
        if ("AOOV" in identified_issues) and ("vietnam" in claim_text):
            identified_issues.add("AOIV")
            identified_issues.remove("AOOV")
        if ("PTSD/1" in identified_issues) and ("non combat" in claim_text):
            identified_issues.add("PTSD/2")
            identified_issues.remove("PTSD/1")
        return list(identified_issues)

    def classify(self, text: str):
        cleaned_text = utils.clean_text(text)
        list_matches = self.check_list(cleaned_text)
        spelling_matches = utils.find_similar(cleaned_text, self.si_map)
        matches = list_matches + spelling_matches
        match_results = []
        for match in matches:
            special_issue = SpecialIssue(text=match)
            match_results.append(special_issue)
        return match_results


@app.post("/", response_model=List[List[SpecialIssue]])
def get_special_issues(claim_text_list: List[str]):
    classifier = SpecialIssuesClassifier()
    return [classifier.classify(claim_text) for claim_text in claim_text_list]
