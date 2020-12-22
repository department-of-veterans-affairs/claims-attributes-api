import docker
import pytest
import sys

@pytest.fixture
def docker_client():
    return docker.from_env()

def test_api(docker_client):
    print("Running API tests...")
    result = docker_client.containers.run("api:test", "regression-test")
    print(f"Result: {result}")

def test_flashes(docker_client):
    print("Running Flashes tests...")
    result = docker_client.containers.run("flashes:test", "regression-test")
    print(f"Result: {result}")

def test_special_issues(docker_client):
    print("Running Special Issues tests...")
    result = docker_client.containers.run("specialissues:test", "regression-test")
    print(f"Result: {result}")

def test_classifier(docker_client):
    print("Running Classifier tests...")
    result = docker_client.containers.run("classifier:test", "regression-test")
    print(f"Result: {result}")

