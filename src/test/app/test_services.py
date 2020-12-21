import docker
import pytest
import sys

@pytest.fixture
def docker_client():
    return docker.from_env()

def test_flashes(docker_client):
    print("Running Flashes tests...")
    result = docker_client.containers.run("flashes:latest", "regression-test")
    print(f"Result: {result}")

def test_special_issues(docker_client):
    print("Running Special Issues tests...")
    result = docker_client.containers.run("special_issues:latest", "regression-test")
    print(f"Result: {result}")

def test_classifier(docker_client):
    print("Running Classifier tests...")
    docker_client.containers.run("classifier:latest", "regression-test")
    print(f"Result: {result}")

