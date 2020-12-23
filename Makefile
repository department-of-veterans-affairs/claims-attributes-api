SHELL := /bin/bash
.PHONY: local-build local-build-macos local-run local-test docker-dev docker-prod docker-test docker-base-images clean 
POETRY:=$(shell which poetry || echo install poetry. see https://python-poetry.org/)
DOCKER:=$(shell which docker || echo install docker. see https://docs.docker.com/get-docker/)
DOCKER_COMPOSE:=$(shell which docker-compose || echo install docker-compose. see https://docs.docker.com/compose/install/)
UNAME_S := $(shell uname -s)

CERT_FILE = cacert.pem
BASE_APPLICATION_IMAGE = va-python-application-base

all:
	echo "No Action"

docker-all: docker-dev docker-prod docker-test

# We need to generate a local cert file to match the server's setup
cert: $(CERT_FILE)

$(CERT_FILE):
	@echo "Copying cert file from python certifi module : $(CERT_FILE)"
	$(eval CERT_FILE_ORIGIN := $(shell python -m certifi))
	cp $(CERT_FILE_ORIGIN) $(CERT_FILE)
	cp $(CERT_FILE) ./src/api_service/
	cp $(CERT_FILE) ./src/classifier_service/
	cp $(CERT_FILE) ./src/flashes_service/
	cp $(CERT_FILE) ./src/special_issues_service/

local: cert local-build local-run

local-build:
	for project in api_service classifier_service flashes_service special_issues_service testing_service ; do \
		echo "Installing $$project ..."; cd ./src/$$project ; $(POETRY) install ; cd ../..; \
	done

local-run: local-run-api local-run-classifier local-run-flashes local-run-special-issues

local-run-api:
	cd ./src/api_service ; $(POETRY) run uvicorn app.main:app --reload --port 8000

local-run-classifier:
	cd ./src/classifier_service ; $(POETRY) run uvicorn app.main:app --reload --port 8001

local-run-flashes:
	cd ./src/flashes_service ; $(POETRY) run uvicorn app.main:app --reload --port 8002

local-run-special-issues:
	cd ./src/special_issues_service ; $(POETRY) run uvicorn app.main:app --reload --port 8003

local-test:
	for project in api_service classifier_service flashes_service special_issues_service testing_service ; do \
		echo "Testing $$project ..."; cd ./src/$$project ; $(POETRY) run pytest -sv --cov=app --cov-report=xml --junitxml=test.xml  ; cd ../..; \
	done

docker-dev: cert docker-base-images
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

docker-prod: cert docker-base-images
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

docker-test: cert docker-base-images
	docker-compose -f docker-compose.yml -f docker-compose.test.yml build
	$(POETRY) run pytest -sv --cov=app --cov-report=xml --junitxml=test.xml 

docker-base-images:
	$(DOCKER) build --target "builder-base" -t "$(BASE_APPLICATION_IMAGE):builder" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "development" -t "$(BASE_APPLICATION_IMAGE):development" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "test" -t "$(BASE_APPLICATION_IMAGE):test" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "production" -t "$(BASE_APPLICATION_IMAGE):production" ./docker/$(BASE_APPLICATION_IMAGE)

docker-clean:
	ECS_IMAGES := $(shell docker images --filter=reference="533575416491.dkr.ecr.us-gov-west-1.amazonaws.com*" -q)
	$(DOCKER) rmi $(ECS_IMAGES)

docker-push:
	ECS_IMAGES := $(shell docker images --filter=reference="533575416491.dkr.ecr.us-gov-west-1.amazonaws.com*" -q)
	$(DOCKER) push $(ECS_IMAGES)

clean:
	$(DOCKER) rm -f api_dev api_prod || true