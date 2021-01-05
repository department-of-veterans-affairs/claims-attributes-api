import pytest
import sys
from app.settings import settings
import requests
from caapi_shared.schemas import (
    Prediction
)
from urlparse import urlparse, urlunparse

def test_predict():
    api_url = urlunsplit(scheme=settings.deployment_test_protocol,
                         netloc=settings.deployment_test_host,
                         path="/benefits-claims-attributes/v1/",
                         params='',
                         query='',
                         fragment='')

    claim_input =  {
        "claim_text": [
            "Ringing in my ear",
            "cancer due to agent orange",
            "p.t.s.d from gulf war",
            "recurring nightmares",
            "skin condition because of homelessness",
        ]
    }
    response = requests.post(api_url, claim_input)
    assert response.status_code == 200
    response = Prediction.parse_obj(response.json())
    assert isinstance(response, Prediction)
    assert len(response.contentions) == 5

def test_docs():
    doc_url = urlunsplit(scheme=settings.deployment_test_protocol,
                         netloc=settings.deployment_test_host,
                         path="/benefits-claims-attributes/v1/docs/openapi.json",
                         params='',
                         query='',
                         fragment='')
    response = requests.get(doc_url)
    assert response.status_code == 200
    output = response.json()
    assert output["info"]["title"] == "Claims Attributes API"

def test_healthcheck():
    healtcheck_url = urlunsplit(scheme=settings.deployment_test_protocol,
                         netloc=settings.deployment_test_host,
                         path="/benefits-claims-attributes/v1/healthcheck",
                         params='',
                         query='',
                         fragment='')
    assert response.status_code == 200
    assert response.json() == "App OK"

if __name__ == "__main__":
    pytest.main(["-sv"])