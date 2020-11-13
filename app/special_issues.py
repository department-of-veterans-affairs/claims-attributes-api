from .utils import clean_text, find_similar
from .schemas import SpecialIssue

spi = {
    "als": "ALS",
    "amyotrophic lateral sclerosis": "ALS",
    "agent orange": "AOOV",
    "ao": "AOOV",
    "herbicide": "AOOV",
    "asbestos": "ASB",
    "asbestosis": "ASB",
    "gulf war": "GW",
    "burn pits": "GW",
    "hepatitis c": "HEPC",
    "hep c": "HEPC",
    "hepatitus c": "HEPC",
    "hiv": "HIV",
    "mustard": "MG",
    "mst": "MST",
    "sexual trauma": "MST",
    "sexual assault": "MST",
    "prisoner": "POW",
    "pow": "POW",
    "ptsd": "PTSD/1",
    "post traumatic stress": "PTSD/1",
    "p t s d": "PTSD/1",
    "posttraumatic stress": "PTSD/1",
    "postraumatic stress": "PTSD/1",
    "pts": "PTSD/1",
    "shell shock": "PTSD/1",
    "stress post traumatic": "PTSD/1",
    "stress disorder": "PTSD/1",
    "personal trauma": "PTSD/3",
    "acquired psychiatric": "PTSD/3",
    "radiation": "RDN",
    "sarcoidosis": "SARCO",
    "tbi": "TBI",
    "t b i": "TBI",
    "traumatic brain injury": "TBI",
    "c 123": "C123",
    "c123": "C123",
}


def find_special_issues(x: str):
    issues = []
    for fl in spi.keys():
        if (fl in x) and (spi[fl] not in issues):
            issues.append(spi[fl])
    if ("AOOV" in issues) and ("vietnam" in x):
        issues.append("AOIV")
        issues.remove("AOOV")
    if ("PTSD/1" in issues) and ("non combat" in x):
        issues.append("PTSD/2")
        issues.remove("PTSD/1")
    return issues


def get_special_issues(text: str) -> [SpecialIssue]:
    special_issues = find_special_issues(clean_text(text)) + find_similar(
        clean_text(text), spi
    )
    return [{"text": special_issue} for special_issue in special_issues]
