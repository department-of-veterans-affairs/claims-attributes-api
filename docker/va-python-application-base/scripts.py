import subprocess


def test():
    """
    Run all tests for this module
    """
    subprocess.run(["pytest", "-sv", "--cov=app", "--cov-report=xml", "--junitxml=test.xml" ])


def server():
    """
    Run the server in prod mode
    """
    subprocess.run(
        ["poetry", "run", "uvicorn", "app.main:app", "--reload"]
    )
