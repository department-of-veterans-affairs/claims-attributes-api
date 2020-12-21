.PHONY: local-build local-build-macos local-run local-test docker-dev docker-prod docker-test docker-base-images clean dc-dev

POETRY:=$(shell which poetry || echo install poetry. see https://python-poetry.org/)
DOCKER:=$(shell which docker || echo install docker. see https://docs.docker.com/get-docker/)
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
	$(POETRY) install

local-run: local-build
	$(POETRY) run uvicorn claims_attributes.main:app --reload

local-test:
	$(POETRY) run pytest -sv

docker-dev: cert docker-base-images
	$(DOCKER) build --target development -t api:dev .
	$(DOCKER) run -d --name api_dev -p 8000:80 api:dev

dc-dev: cert docker-base-images
	docker-compose up

docker-prod: cert docker-base-images
	$(DOCKER) build --target production -t api:prod .
	$(DOCKER) run -d --name api_prod -p 8001:80 api:prod

docker-test: cert docker-base-images
	$(DOCKER) build --target production -t api:test .
	$(DOCKER) run --rm --network host api:testing regression-test
	$(DOCKER) run --rm --network host api:testing smoke-test

docker-base-images:
	$(DOCKER) build --target "builder-base" -t "$(BASE_APPLICATION_IMAGE):builder" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "development" -t "$(BASE_APPLICATION_IMAGE):development" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "test" -t "$(BASE_APPLICATION_IMAGE):test" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "production" -t "$(BASE_APPLICATION_IMAGE):production" ./docker/$(BASE_APPLICATION_IMAGE)

clean:
	$(DOCKER) rm -f api_dev api_prod || true