from pydantic import BaseSettings
from importlib_resources import files


class Settings(BaseSettings):
    VECTORIZER_URI: str
    CLASSIFIER_URI: str
    FLASHES_URI: str
    SPECIAL_ISSUES_URI: str


settings_file = files("app").joinpath("dev.env")
settings = Settings(_env_file=settings_file)
