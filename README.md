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

1. Install pyenv, then python version 3.8.6 (note that as of this commit, scikit-learn has a bug in compiling against 3.9.0 )

   ```sh
   brew install pyenv
   pyenv install 3.8.6
   pyenv local 3.8.6
   ```

1. Install Poetry

   This project uses [Poetry](https://python-poetry.org/) for managing dependencies and packaging. It is configured via the file `pyproject.toml`, and dependencies are stored in `poetry.lock`. To add additional dependencies, use `poetry add` to resolve the dependency tree.

   ```sh
   curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
   ```

1. Use poetry to install dependencies

   ```sh
   poetry install
   ```

1.  Install certifi module, if not already installed

   ```sh
   pip install certifi
   ```


#### Run

Run `make -j4 local` to run the app locally. Since this project is built in microservices, the `-j4` flag is required to run all services concurrently.

This installs a necessary certificate file, then uses a function in `scripts.py` defined in `pyproject.toml`. Under the hood, FastAPI uses the gunicorn ASGI server to serve content.

#### VSCode

Each service within the bundle contains a `settings.json` and `launch.json` to allow for smooth VSCode debugging.

To enable this, the `poetry.toml` file within each service specifies the `in-project` option in order to install a virtualenv into `.venv` within every given service directory. By default it is included in `gitignore`! All that is necessary is to call `poetry update` and then `code .` for each project within the directory, and run the `debug` target to enable breakpoints, linting, and formatting support.

### Docker

This project builds with Docker [multistage](https://docs.docker.com/develop/develop-images/multistage-build/) builds via the `Dockerfile`.

_NOTE!_ All docker builds require you to use a `cacert.pem` file, to match the way certificates work on the build server, which self-signs. To generate this, you can run `make cert`. This command requires the python `certifi` [module](https://pypi.org/project/certifi/) to obtain Mozilla's root certificates and copy this when running locally - `poetry install` installs this dependency for you. Note also that over time these need to be updated - to do this you'll need to remove `cacert.pem` and re-run `make cert`, if you get any `SSL` errors when building.

#### Build

There are three different docker flavors available, depending on what you want to do: `dev`, `prod`, and `test`.

1. `dev` : for local development using docker. To build and run, run `make docker-dev`. Will continue running until you quit it.
2. `prod` : for building and running a version of the app optimized for production. This build will be run on the build server. To build and run, run `make docker-prod`. Will continue running until you quit it.
3. `test` : for building and running a version of the test container with an entrypoint for testing that is used by our build server/deployer as part of blue/green deployment. See more [here](https://github.com/department-of-veterans-affairs/health-apis-deployer/blob/qa/deployment-unit.md).

#### Run

The above `Makefile` commands will both run and test. See the Makefile for instructions, but you'll need to expose a port as in the below:

```sh
docker run --name api -p 8000:80 api:latest
```

### Jenkins

VA corporate CI jobs run on Jenkins, with a build agent built with its own Dockerfile. We keep the `Jenkinsfile` simple by using the `standardShellBuild` shared function, and relying on parent Docker images in the Octopus [repo(private)](https://github.com/department-of-veterans-affairs/health-apis-docker-octopus/tree/master).

#### Build

Standard Shell build:

1. Builds our `Dockerfile.build` agent image
2. Runs `build.sh` on it, which builds our image, plus its test image, via the `Dockerfile`
3. Deploys both the image and test image to ECR.

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
curl -H "Content-Type: application/json" -X POST -d '{"claim_text":["Ringing in my ear", "cancer due to agent orange", "p.t.s.d from gulf war", "recurring nightmares", "skin condition because of homelessness"]}' http://localhost:8000/services/claims-attributes/v1/
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
