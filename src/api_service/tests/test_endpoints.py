from fastapi.testclient import TestClient
from app.main import app
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
