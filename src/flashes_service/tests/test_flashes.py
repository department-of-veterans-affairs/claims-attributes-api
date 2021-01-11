import pytest
from app.main import app, FlashesClassifier
from caapi_shared.schemas import Flash, FlashesServiceOutput
from fastapi.testclient import TestClient

from tests.settings import settings as test_settings


@pytest.fixture
def global_config():
    return {
        "input_json": {"claim_text": ["skin condition because of homelessness", "ALS"]},
        "flash_uri": "/",
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


def test_flashes_endpoint(client, global_config):
    response = client.post(global_config["flash_uri"], json=global_config["input_json"])
    assert response.status_code == 200
    response = FlashesServiceOutput.parse_obj(response.json())
    assert isinstance(response, FlashesServiceOutput)
    assert len(response.flashes) == 2
    for flash_list in response.flashes:
        assert isinstance(response, Flash)
        assert len(flash_list) == 1
        flash = flash_list[0]
        assert flash.text is not None


def test_flashes_classifier_keywords(client):
    classifier = FlashesClassifier()
    assert classifier.check_keywords("hardship") == {"Hardship"}
    assert classifier.check_keywords("seriously injured") == {
        "Seriously Injured/Very Seriously Injured"
    }
    assert classifier.check_keywords("terminally ill") == {"Terminally Ill"}
    assert classifier.check_keywords("homeless") == {"Homeless"}
    assert classifier.check_keywords("purple heart") == {"Purple Heart"}
    assert (
        classifier.check_keywords("pow")
        == classifier.check_keywords("prisoner of war")
        == classifier.check_keywords("p o w")
        == {"POW"}
    )
    assert classifier.check_keywords("medal of honor") == {"Medal of Honor"}
    assert (
        classifier.check_keywords("amyotrophic lateral sclerosis")
        == classifier.check_keywords("als")
        == classifier.check_keywords("a l s")
        == {"Amyotrophic Lateral Sclerosis"}
    )
    assert classifier.check_keywords("emergency care") == {"Emergency Care"}


def test_flashes_classifier_classify(client):
    classifier = FlashesClassifier()
    assert classifier.classify("ALS") == [Flash(text="Amyotrophic Lateral Sclerosis")]


def test_flashes_classifier_nonexistent_classify(client):
    classifier = FlashesClassifier()
    assert classifier.classify("Does not exist") == []