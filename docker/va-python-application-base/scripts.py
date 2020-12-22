import subprocess


def test():
    """
    Run all tests for this module
    """
    subprocess.run(["pytest", "-sv"])


def server():
    """
    Run the server in prod mode
    """
    subprocess.run(
        ["poetry", "run", "uvicorn", "app.main:app", "--reload"]
    )
