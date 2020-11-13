# Claims Attributes API

## Description

This API uses Natural Language Understading to infer 526 Benefit Claims Attributes, like classification, flashes and special issues, from text and other features.

## Setup

*Important!*
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

   It is recommended to install [pyenv](https://github.com/pyenv/pyenv) and [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) in order to isolate python versions and dependencies. You can still build without these using system python, but they will keep things cleaner

   ```sh
   brew install pyenv
   brew install pyenv-virtualenv
   echo 'eval "$(pyenv init -)\n$(pyenv virtualenv-init -)\n"' >> ~/.bash_profile
   pyenv install  3.7.3
   pyenv virtualenv  3.7.3 claims-attributes-api-3.7.3
   pyenv activate claims-attributes-api-3.7.3
   exec "$SHELL"
   ```

   Then to install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

#### Run

Run `uvicorn app.main:app --reload` to run the Uvicorn server. 

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

* It uses [git-lfs](https://git-lfs.github.com/) for storing large language modeling files
* It uses [FastAPI](https://fastapi.tiangolo.com/) for quick generation of API documentation
* It uses two pickled [Scikit-Learn](https://scikit-learn.org/stable/) model files, one for vectorizing input and another for associating claims text with numeric classifications

## Example Run

```sh
curl -H "Content-Type: application/json" -X POST -d '{"claim_text":["Ringing in my ear", "cancer due to agent orange", "p.t.s.d from gulf war", "recurring nightmares", "skin condition because of homelessness"]}' localhost:8000/benefits-claims-attributes/
```

The response should looks like this:

```json
{
   "contentions" : [
      {
         "classification" : {
            "text" : "hearing loss",
            "code" : "3140",
            "confidence" : 96
         },
         "specialIssues" : [],
         "flashes" : [],
         "originalText" : "Ringing in my ear"
      },
      {
         "classification" : {
            "text" : "cancer - genitourinary",
            "code" : "8935",
            "confidence" : 96
         },
         "originalText" : "cancer due to agent orange",
         "flashes" : [],
         "specialIssues" : [
            {
               "text" : "AOOV"
            }
         ]
      },
      {
         "specialIssues" : [
            {
               "text" : "GW"
            },
            {
               "text" : "PTSD/1"
            }
         ],
         "flashes" : [],
         "originalText" : "p.t.s.d from gulf war",
         "classification" : {
            "confidence" : 96,
            "code" : "8989",
            "text" : "mental disorders"
         }
      },
      {
         "classification" : {
            "confidence" : 96,
            "code" : "8989",
            "text" : "mental disorders"
         },
         "originalText" : "recurring nightmares",
         "flashes" : [],
         "specialIssues" : []
      },
      {
         "classification" : {
            "text" : "skin",
            "confidence" : 96,
            "code" : "9016"
         },
         "flashes" : [
            {
               "text" : "Homeless"
            }
         ],
         "originalText" : "skin condition because of homelessness",
         "specialIssues" : []
      }
   ]
}
```
