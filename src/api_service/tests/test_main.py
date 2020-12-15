from fastapi.testclient import TestClient
from claims_attributes.main import app
import pytest

client = TestClient(app)


def test_docs():
    response = client.get("/benefits-claims-attributes/v1/docs/openapi.json")
    assert response.status_code == 200
    output = response.json()
    assert output["info"]["title"] == "Claims Attributes API"


def test_healthcheck():
    response = client.get("/benefits-claims-attributes/v1/healthcheck")
    assert response.status_code == 200
    assert response.json() == "App OK"


# We set a bogus confidence to avoid testing model specifics
# See more here: https://docs.pytest.org/en/latest/parametrize.html#pytest-mark-parametrize
@pytest.mark.parametrize("bogus_confidence",
                         [96.0])
def test_predict(bogus_confidence):
    response = client.post(
        "/benefits-claims-attributes/v1/",
        json={
            "claim_text": [
                "Ringing in my ear",
                "cancer due to agent orange",
                "p.t.s.d from gulf war",
                "recurring nightmares",
                "skin condition because of homelessness",
            ]
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "contentions": [
            {
                "specialIssues": [],
                "flashes": [],
                "originalText": "Ringing in my ear",
                "classification": {
                    "text": "hearing loss",
                    "confidence": float(f"{bogus_confidence}"),
                    "code": "3140",
                },
            },
            {
                "flashes": [],
                "specialIssues": [{"text": "AOOV"}],
                "classification": {
                    "code": "8935",
                    "confidence": float(f"{bogus_confidence}"),
                    "text": "cancer - genitourinary",
                },
                "originalText": "cancer due to agent orange",
            },
            {
                "originalText": "p.t.s.d from gulf war",
                "classification": {
                    "text": "mental disorders",
                    "code": "8989",
                    "confidence": float(f"{bogus_confidence}"),
                },
                "flashes": [],
                "specialIssues": [{"text": "GW"}, {"text": "PTSD/1"}],
            },
            {
                "specialIssues": [],
                "flashes": [],
                "originalText": "recurring nightmares",
                "classification": {
                    "text": "mental disorders",
                    "code": "8989",
                    "confidence": float(f"{bogus_confidence}"),
                },
            },
            {
                "classification": {"confidence": float(f"{bogus_confidence}"), "code": "9016", "text": "skin"},
                "originalText": "skin condition because of homelessness",
                "specialIssues": [],
                "flashes": [{"text": "Homeless"}],
            },
        ]
    }
