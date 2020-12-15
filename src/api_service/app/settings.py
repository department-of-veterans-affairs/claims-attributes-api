from pydantic import BaseSettings
from importlib_resources import files


class Settings(BaseSettings):
    CLASSIFIER_URI: str
    FLASHES_URI: str
    SPECIAL_ISSUES_URI: str


settings_file = files("app").joinpath("local.env")
settings = Settings(_env_file=settings_file)
