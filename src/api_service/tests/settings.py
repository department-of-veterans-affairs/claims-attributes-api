from pydantic import BaseSettings
from importlib_resources import files
import os


class Settings(BaseSettings):
    # These come from the Deployer
    deployment_test_protocol: str = "http"
    deployment_test_host: str = "testserver"
    deployment_test_port: int = 80
    use_mock: bool = True

    class Config:
        env_file = files("tests").joinpath("local.env")


settings = Settings()
