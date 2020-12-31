import docker
import pytest
import sys
from app.settings import settings

@pytest.fixture
def docker_client():
    tls_config = docker.tls.TLSConfig(ca_cert='/app/cacert.pem')
    client = docker.DockerClient(base_url='unix://var/run/docker.sock', tls=tls_config)
    print(f"Images: {client.images.list()}")
    print(f"Containers: {client.containers.list()}")
    return client

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

