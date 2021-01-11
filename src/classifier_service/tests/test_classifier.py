from fastapi.testclient import TestClient
from tests.settings import settings as test_settings
from app.main import app
from caapi_shared.schemas import ClassifierServiceOutput, Classification
import pytest


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
        "classify_uri": "/",
    }


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


def test_startup(client, global_config):
    # Use this to get startup events, as specified here: https://fastapi.tiangolo.com/advanced/testing-events/
    with client as client:
        response = client.post(
            global_config["classify_uri"], json=global_config["input_json"]
        )
        assert response.status_code == 200
        response = ClassifierServiceOutput.parse_obj(response.json())
        assert isinstance(response, ClassifierServiceOutput)
        assert len(response.classifications) == 5
        for classification in response.classifications:
            assert classification.text is not None
            assert classification.code is not None
            assert classification.confidence is not None