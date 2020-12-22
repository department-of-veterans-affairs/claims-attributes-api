from pydantic import BaseSettings
from importlib_resources import files
import os

class Settings(BaseSettings):
    classifier_uri: str
    flashes_uri: str
    special_issues_uri: str

    class Config:
        env_file = files("app").joinpath(".env.local")

settings = Settings()
