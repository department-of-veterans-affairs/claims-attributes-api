import subprocess


def test():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(
        ['python', '-u', '-m', 'unittest', 'discover']
    )


def server():
    """
    Run all unittests. Equivalent to:
    `poetry run python -u -m unittest discover`
    """
    subprocess.run(
        ['poetry', 'run', 'uvicorn', 'app.main:app', '--reload']
    )
