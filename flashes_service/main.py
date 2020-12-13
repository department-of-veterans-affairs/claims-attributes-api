from caapi_shared.utils import clean_text, find_similar
from caapi_shared.schemas import Flash
from fastapi import FastAPI

app = FastAPI()

def find_flashes(x):
    flashes = []
    if "hardship" in x:
        flashes.append("Hardship")
    if "seriously injured" in x:
        flashes.append("Seriously Injured/Very Seriously Injured")
    if "terminally ill" in x:
        flashes.append("Terminally Ill")
    if "homeless" in x:
        flashes.append("Homeless")
    if "purple heart" in x:
        flashes.append("Purple Heart")
    if ("pow" in x) or ("prisoner of war" in x) or ("p o w" in x):
        flashes.append("POW")
    if "medal of honor" in x:
        flashes.append("Medal of Honor")
    if ("amyotrophic lateral sclerosis" in x) or ("als" in x) or ("a l s" in x):
        flashes.append("Amyotrophic Lateral Sclerosis")
    if "emergency care" in x:
        flashes.append("Emergency Care")
    return flashes


flashesD = {
    "hardship": "Hardship",
    "seriously injured": "Seriously Injured/Very Seriously Injured",
    "terminally ill": "Terminally Ill",
    "homeless": "Homeless",
    "purple heart": "Purple Heart",
    "pow": "POW",
    "prisoner of war": "POW",
    "p o w": "POW",
    "medal of honor": "Medal of Honor",
    "amyotrophic lateral sclerosis": "Amyotrophic Lateral Sclerosis",
    "als": "Amyotrophic Lateral Sclerosis",
    "a l s": "Amyotrophic Lateral Sclerosis",
    "emergency care": "Emergency Care",
}


@app.get("/")
def get_flashes(text) -> [Flash]:
    flashes = find_flashes(clean_text(text)) + find_similar(clean_text(text), flashesD)
    return [{"text": flash} for flash in flashes]  # leaving off confidence for now

