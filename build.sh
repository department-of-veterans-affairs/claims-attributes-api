#!/usr/bin/env bash
set -euo pipefail
ECR_REGISTRY=533575416491.dkr.ecr.us-gov-west-1.amazonaws.com
COMMON_PREFIX=benefits-apis-claims-attributes
BASE_APPLICATION_IMAGE=va-python-application-base

# Copy in cacert file to enable network operations w/ self-signed certificate
echo "Copying cert file from ${SSL_CERT_FILE}..."
cp $SSL_CERT_FILE ./docker/$BASE_APPLICATION_IMAGE

# Build our base images - until this is centrally hosted, we build and reference locally in each constituent dockerfile
echo "Building base images..."
docker build --target "builder-base" -t $BASE_APPLICATION_IMAGE:builder ./docker/$BASE_APPLICATION_IMAGE
docker build --target "production" -t $BASE_APPLICATION_IMAGE:production ./docker/$BASE_APPLICATION_IMAGE
docker build --target "test" -t $BASE_APPLICATION_IMAGE:test ./docker/$BASE_APPLICATION_IMAGE

echo "Building app with Docker-compose..."
docker-compose build

if [ $RELEASE == true ]
then
  echo "Release config. Pushing images..."
  aws ecr get-login-password --region us-gov-west-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

  # Our "API" image is just named for the service itself. Push that first
  echo "Pushing api image"
  docker push $ECR_REGISTRY/$COMMON_PREFIX:$VERSION
  for SERVICE in classifier flashes special-issues
  do
    echo "Pushing image ${SERVICE}"
    docker push "$ECR_REGISTRY/$COMMON_PREFIX-$SERVICE-service:$VERSION"
  done
  echo "Pushing test image"
  docker push $ECR_REGISTRY/$COMMON_PREFIX-test:$VERSION
fi

echo "Removing images..."
docker rmi $DEPLOY_IMAGE $TEST_IMAGE