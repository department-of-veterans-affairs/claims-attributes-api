from pydantic import BaseSettings
from importlib_resources import files
import os

class Settings(BaseSettings):
    classifier_image: str
    flashes_image: str
    special_issues_image: str
    api_image: str

    class Config:
        env_file = files("app").joinpath("local.env")

settings = Settings()
