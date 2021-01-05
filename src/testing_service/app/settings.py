from pydantic import BaseSettings
from importlib_resources import files
import os

class Settings(BaseSettings):
    # These come from the Deployer
    deployment_test_protocol: str
    deployment_test_host: str
    deployment_test_port: int

    # These are ours
    classifier_uri: str
    flashes_uri: str
    special_issues_uri: str
    api_uri: str

    class Config:
        env_file = files("app").joinpath("local.env")

settings = Settings()
