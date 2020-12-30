.PHONY: local-build local-build-macos local-run local-test docker-dev docker-staging docker-prod docker-test docker-base-images docker-clean docker-push clean 
POETRY:=$$(which poetry || echo "install poetry. see https://python-poetry.org/")
DOCKER:=$$(which docker || echo "install docker. see https://docs.docker.com/get-docker/")
DOCKER_COMPOSE:=$$(which docker-compose || echo "install docker-compose. see https://docs.docker.com/compose/install/")

# Note this will change value over time, as it is defined with "=" instead of ":="
ECS_IMAGES=$$(docker images --filter=reference="533575416491.dkr.ecr.us-gov-west-1.amazonaws.com/benefits-apis-claims-attributes*:*" --format "{{.Repository}}:{{.Tag}}")

CERT_FILE = ./docker/va-python-application-base/cacert.pem
BASE_APPLICATION_IMAGE = va-python-application-base

all:
	echo "No Action"

docker-all: docker-dev docker-prod docker-test

# We need to generate a local cert file to match the server's setup
cert: $(CERT_FILE)

$(CERT_FILE):
	@echo "Copying cert file from python certifi module : $(CERT_FILE)"
	cp $$(python -m certifi) $(CERT_FILE)

local: cert local-build local-run

local-build:
	for project in api_service classifier_service flashes_service special_issues_service testing_service ; do \
		echo "Installing $$project ..."; cd ./src/$$project ; $(POETRY) install ; cd ../..; \
	done

# Tip: run this with `make -j4 local-run` to run all services concurrently
local-run: local-run-api local-run-classifier local-run-flashes local-run-special-issues

local-run-api:
	cd ./src/api_service ; $(POETRY) run uvicorn app.main:app --reload --port 8000

local-run-classifier:
	cd ./src/classifier_service ; $(POETRY) run uvicorn app.main:app --reload --port 8001

local-run-flashes:
	cd ./src/flashes_service ; $(POETRY) run uvicorn app.main:app --reload --port 8002

local-run-special-issues:
	cd ./src/special_issues_service ; $(POETRY) run uvicorn app.main:app --reload --port 8003

local-test: local-build
	for project in api_service classifier_service flashes_service special_issues_service ; do \
		echo "Testing $$project ..."; cd ./src/$$project ; $(POETRY) run pytest -sv --cov=app --cov-report=xml --junitxml=test.xml  ; cd ../..; \
	done

docker-dev: cert docker-base-images
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build

docker-test: cert docker-base-images
	docker-compose -f docker-compose.yml -f docker-compose.test.yml build
	docker run -v /var/run/docker.sock:/var/run/docker.sock --rm --network host testing:test regression-test

docker-staging: docker-base-images
	export VERSION=staging; $(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.staging.yml up --build

docker-prod: docker-base-images
	$(DOCKER_COMPOSE) -f docker-compose.yml -f docker-compose.prod.yml build

docker-base-images:
	$(DOCKER) build --target "builder-base" -t "$(BASE_APPLICATION_IMAGE):builder" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "development" -t "$(BASE_APPLICATION_IMAGE):development" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "test" -t "$(BASE_APPLICATION_IMAGE):test" ./docker/$(BASE_APPLICATION_IMAGE)
	$(DOCKER) build --target "production" -t "$(BASE_APPLICATION_IMAGE):production" ./docker/$(BASE_APPLICATION_IMAGE)

docker-clean:
	@echo "Removing the following ECS IMAGES: $(ECS_IMAGES)"
	if test "$(ECS_IMAGES)"; then \
		$(DOCKER) rmi $(ECS_IMAGES); \
	else \
		echo "ECS_IMAGES Empty"; \
	fi;

docker-push:
	@echo "Pushing the following ECS IMAGES: $(ECS_IMAGES)"
	if test "$(ECS_IMAGES)"; then \
		for IMAGE in $(ECS_IMAGES); do \
			 $(DOCKER) push $$IMAGE; \
		done \
	else \
		echo "ECS_IMAGES Empty"; \
	fi;

clean:
	$(DOCKER) rm -f api_dev api_prod || true