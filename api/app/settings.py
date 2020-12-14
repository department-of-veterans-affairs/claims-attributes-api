from pydantic import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    VECTORIZER_URI: str
    CLASSIFIER_URI: str
    FLASHES_URI: str
    SPECIAL_ISSUES_URI: str


settings = Settings(_env_file=Path("api/dev.env"))
