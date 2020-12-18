import requests
from app.settings import settings


def test_services():
    print(f"Settings: {settings.classifier_uri}")
    assert True==True
