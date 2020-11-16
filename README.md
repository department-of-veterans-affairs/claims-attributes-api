# Claims Attributes API

## Description

This API uses Natural Language Understading to infer 526 Benefit Claims Attributes, like classification, flashes and special issues, from text and other features.

## Setup

_Important!_
This project uses [git-lfs](https://git-lfs.github.com/) for storing large language modeling files. It is necessary to install this tool locally in order to properly work with these datafiles. Do so by running:

```sh
brew install git-lfs
git lfs install
```

Please run the above before checkout. If you checkout first and install `gif-lfs` later, you can run the below to check out the files:

```sh
git lfs checkout
```

When you work with these files going forward they will appear to be their binary versions on disk, but a pre-commit hook will convert them to file pointers.

## Building + Running

### Local

#### Build

1. Install

   This project uses [Poetry](https://python-poetry.org/) for managing dependencies and packaging. It is configured via the file `pyproject.toml`, and dependencies are stored in `poetry.lock`. To add additional dependencies, use `poetry add` to resolve the dependency tree.

   ```sh
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
   ```

2. Use poetry to install dependencies

   ```sh
   poetry install
   ```

#### Run

Run `poetry run server` to run the app. This uses a function in `scripts.py` defined in `pyproject.toml`. Under the hood, FastAPI uses the gunicorn ASGI server to serve content.

### Docker

This project builds with Docker [multistage](https://docs.docker.com/develop/develop-images/multistage-build/) builds via the `Dockerfile`.

#### Build

```sh
docker build -t api .
```

#### Run

```sh
docker run --name api -p 8000:80 api:latest
```

### Jenkins

VA corporate CI jobs run on Jenkins, with a build agent built with its own Dockerfile. We keep the `Jenkinsfile` simple by using the `standardShellBuild` shared function, and relying on parent Docker images in the Octopus [repo(private)](https://github.com/department-of-veterans-affairs/health-apis-docker-octopus/tree/master).

#### Build

Standard Shell build:

1. Builds our `Dockerfile.build` agent image
2. Runs `build.sh` on it, which builds our image via the `Dockerfile`
3. Deploys the image to ECR

See more about this setup [here (Private Repo)](https://github.com/department-of-veterans-affairs/health-apis-devops/tree/master/ci).

#### Run

This job posts the repository to ECR, from where you can clone it and run locally with `docker run`.

## Technical Background

- This project uses the [Poetry](https://python-poetry.org/) dependency management and packaging tool
- It uses [git-lfs](https://git-lfs.github.com/) for storing large language modeling files
- It uses [FastAPI](https://fastapi.tiangolo.com/) for quick generation of API documentation
- It uses the [uvicorn-gunicorn-fastapi-docker](https://github.com/tiangolo/uvicorn-gunicorn-fastapi-docker) docker image as a base image to configure and run the ASGI server
- It uses two pickled [Scikit-Learn](https://scikit-learn.org/stable/) model files, one for vectorizing input and another for associating claims text with numeric classifications

## Example Run

```sh
curl -H "Content-Type: application/json" -X POST -d '{"claim_text":["Ringing in my ear", "cancer due to agent orange", "p.t.s.d from gulf war", "recurring nightmares", "skin condition because of homelessness"]}' localhost:8000/benefits-claims-attributes/
```

The response should looks like this:

```json
{
  "contentions": [
    {
      "classification": {
        "text": "hearing loss",
        "code": "3140",
        "confidence": 96
      },
      "specialIssues": [],
      "flashes": [],
      "originalText": "Ringing in my ear"
    },
    {
      "classification": {
        "text": "cancer - genitourinary",
        "code": "8935",
        "confidence": 96
      },
      "originalText": "cancer due to agent orange",
      "flashes": [],
      "specialIssues": [
        {
          "text": "AOOV"
        }
      ]
    },
    {
      "specialIssues": [
        {
          "text": "GW"
        },
        {
          "text": "PTSD/1"
        }
      ],
      "flashes": [],
      "originalText": "p.t.s.d from gulf war",
      "classification": {
        "confidence": 96,
        "code": "8989",
        "text": "mental disorders"
      }
    },
    {
      "classification": {
        "confidence": 96,
        "code": "8989",
        "text": "mental disorders"
      },
      "originalText": "recurring nightmares",
      "flashes": [],
      "specialIssues": []
    },
    {
      "classification": {
        "text": "skin",
        "confidence": 96,
        "code": "9016"
      },
      "flashes": [
        {
          "text": "Homeless"
        }
      ],
      "originalText": "skin condition because of homelessness",
      "specialIssues": []
    }
  ]
}
```
