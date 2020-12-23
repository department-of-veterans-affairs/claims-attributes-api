import docker
import pytest
import sys
from app.settings import settings

@pytest.fixture
def docker_client():
    d = docker.from_env()
    print(f"Images: {d.images.list()}")
    print(f"Containers: {d.containers.list()}")
    return d

def test_api(docker_client):
    print("Running API tests...")
    result = docker_client.containers.run(settings.api_image, "regression-test")
    print(f"Result: {result}")

def test_flashes(docker_client):
    print("Running Flashes tests...")
    result = docker_client.containers.run(settings.flashes_image, "regression-test")
    print(f"Result: {result}")

def test_special_issues(docker_client):
    print("Running Special Issues tests...")
    result = docker_client.containers.run(settings.special_issues_image, "regression-test")
    print(f"Result: {result}")

def test_classifier(docker_client):
    print("Running Classifier tests...")
    result = docker_client.containers.run(settings.classifier_image, "regression-test")
    print(f"Result: {result}")

