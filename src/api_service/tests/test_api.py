from fastapi.testclient import TestClient
from app.main import app
import requests
from caapi_shared.schemas import (
    Prediction,
    ClassifierServiceOutput,
    Classification,
    FlashesServiceOutput,
    Flash,
    SpecialIssueServiceOutput,
    SpecialIssue,
)
from app.settings import settings as app_settings
from tests.settings import settings as test_settings
import pytest
import collections


@pytest.fixture
def client():
    from urllib.parse import urlunsplit

    location = (
        f"{test_settings.deployment_test_host}:{test_settings.deployment_test_port}"
    )
    base_url = urlunsplit(
        (test_settings.deployment_test_protocol, location, "", "", "")
    )
    return TestClient(base_url=base_url, app=app)

def mock_responses(requests_mock):
    classifier_output = ClassifierServiceOutput(
        classifications=[
            Classification(text="hearing loss", confidence=96, code="3140"),
            Classification(text="cancer - genitourinary", confidence=96, code="8935"),
            Classification(text="mental disorders", confidence=96, code="8989"),
            Classification(text="mental disorders", confidence=96, code="8989"),
            Classification(text="skin", confidence=96, code="9016"),
        ]
    ).dict()
    requests_mock.post(app_settings.classifier_uri, json=classifier_output)

    flashes_output = FlashesServiceOutput(
        flashes=[[], [], [], [], [Flash(text="Homeless")]]
    ).dict()
    requests_mock.post(app_settings.flashes_uri, json=flashes_output)

    special_issues_output = SpecialIssueServiceOutput(
        special_issues=[
            [],
            [SpecialIssue(text="AOOV")],
            [SpecialIssue(text="GW"), SpecialIssue(text="PTSD/1")],
            [],
            [],
        ]
    ).dict()
    requests_mock.post(app_settings.special_issues_uri, json=special_issues_output)

@pytest.mark.smoke
def test_healthcheck(client):
    response = client.get("/services/claims-attributes/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == "App OK"

def test_docs(client):
    response = client.get("/services/claims-attributes/v1/docs/openapi.json")
    assert response.status_code == 200
    output = response.json()
    assert output["info"]["title"] == "Claims Attributes API"

@pytest.fixture
def global_config():
    return {
        "input_json": {
            "claim_text": [
                "Ringing in my ear",
                "cancer due to agent orange",
                "p.t.s.d from gulf war",
                "recurring nightmares",
                "skin condition because of homelessness",
            ]
        },
        "predict_uri": "/services/claims-attributes/v1/",
    }

def test_predict_working(client, global_config, requests_mock):
    if test_settings.use_mock:
        mock_responses(requests_mock)

    # Use the actual POST for this endpoint
    requests_mock.real_http = True
    response = client.post(
        global_config["predict_uri"], json=global_config["input_json"]
    )
    assert response.status_code == 200
    response = Prediction.parse_obj(response.json())
    assert isinstance(response, Prediction)
    assert len(response.contentions) == 5


def test_predict_broken_services(client, global_config, requests_mock):
    for uri in [
        app_settings.classifier_uri,
        app_settings.flashes_uri,
        app_settings.special_issues_uri,
    ]:
        requests_mock.post(uri, status_code=500)
        with pytest.raises(requests.exceptions.HTTPError):
            requests_mock.real_http = True
            client.post(global_config["predict_uri"], json=global_config["input_json"])
