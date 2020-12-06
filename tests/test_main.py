from fastapi.testclient import TestClient

from claims_attributes.main import app

client = TestClient(app)


def test_docs():
    response = await client.get("/benefits-claims-attributes/v1/docs/openapi.json")
    assert response.status_code == 200
    output = response.json()
    assert output["info"]["title"] == "Site Domain Manager"


async def test_predict():
    response = await client.post(
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
                    "confidence": 96,
                    "code": "3140",
                },
            },
            {
                "flashes": [],
                "specialIssues": [{"text": "AOOV"}],
                "classification": {
                    "code": "8935",
                    "confidence": 96,
                    "text": "cancer - genitourinary",
                },
                "originalText": "cancer due to agent orange",
            },
            {
                "originalText": "p.t.s.d from gulf war",
                "classification": {
                    "text": "mental disorders",
                    "code": "8989",
                    "confidence": 96,
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
                    "confidence": 96,
                },
            },
            {
                "classification": {"confidence": 96, "code": "9016", "text": "skin"},
                "originalText": "skin condition because of homelessness",
                "specialIssues": [],
                "flashes": [{"text": "Homeless"}],
            },
        ]
    }
