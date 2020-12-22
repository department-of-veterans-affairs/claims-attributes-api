import subprocess
import docker

def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(["pytest", "-sv"])


def server():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    client = docker.from_env()
    #client.containers.run(image="classifier:latest", auto_remove=True, command="regression-test")
    #client.containers.run(image="flashes:latest", auto_remove=True, command="regression-test")
    