import pytest
from app.main import app, SpecialIssuesClassifier
from caapi_shared.schemas import SpecialIssue, SpecialIssueServiceOutput
from fastapi.testclient import TestClient

from tests.settings import settings as test_settings


@pytest.fixture
def global_config():
    return {
        "input_json": {
            "claim_text": ["cancer due to agent orange", "p.t.s.d from gulf war"]
        },
        "special_issue_uri": "/",
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


def test_special_issues_endpoint(client, global_config):
    response = client.post(
        global_config["special_issue_uri"], json=global_config["input_json"]
    )
    assert response.status_code == 200
    response = SpecialIssueServiceOutput.parse_obj(response.json())
    assert isinstance(response, SpecialIssueServiceOutput)
    assert len(response.special_issues) == 2

    aoov = response.special_issues[0]
    assert len(aoov) == 1
    assert aoov == [SpecialIssue(text="AOOV")]

    gw_ptsd = response.special_issues[1]
    assert len(gw_ptsd) == 2
    assert SpecialIssue(text="GW") gw_ptsd
    assert SpecialIssue(text="PTSD/1") in gw_ptsd


def test_special_issues_classifier_classify(client):
    classifier = SpecialIssuesClassifier()
    assert classifier.classify("Agent Orange") == [SpecialIssue(text="AOOV")]
    assert classifier.classify("Agent Orange from Vietnam") == [
        SpecialIssue(text="AOIV")
    ]
    assert classifier.classify("PTSD") == [SpecialIssue(text="PTSD/1")]
    assert classifier.classify("Non-combat PTSD") == [SpecialIssue(text="PTSD/2")]
