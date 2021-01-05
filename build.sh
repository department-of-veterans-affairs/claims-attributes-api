#!/usr/bin/env bash
set -euo pipefail
ECR_REGISTRY=533575416491.dkr.ecr.us-gov-west-1.amazonaws.com
BASE_APPLICATION_IMAGE=va-python-application-base

# Copy in cacert file to enable network operations w/ self-signed certificate
echo "Copying cert file from ${SSL_CERT_FILE}..."
cp $SSL_CERT_FILE ./docker/$BASE_APPLICATION_IMAGE

echo "Running unit tests..."
make docker-test

# Build our base images - until this is centrally hosted, we build and reference locally in each constituent dockerfile
echo "Building app with Docker-compose..."
make docker-prod

if [ $RELEASE == true ]
then
  echo "Release config. Pushing images..."
  aws ecr get-login-password --region us-gov-west-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

  # Our "API" image is just named for the service itself. Push that first
  echo "Pushing images"
  make docker-push
fi

echo "Removing images..."
make docker-clean
docker-compose down