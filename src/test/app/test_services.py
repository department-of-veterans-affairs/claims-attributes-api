import requests
from app.settings import settings
import docker

def setup_module(module):
    client = docker.from_env()

def test_services():
    
    print(f"Settings: {settings.classifier_uri}")
    assert True==True
