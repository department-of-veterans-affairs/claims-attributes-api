#!/usr/bin/env bash
set -euo pipefail
ECR_REGISTRY=533575416491.dkr.ecr.us-gov-west-1.amazonaws.com
COMMON_PREFIX=benefits-apis-claims-attributes
BASE_APPLICATION_IMAGE=va-python-application-base

cp $SSL_CERT_FILE ./docker/$BASE_APPLICATION_IMAGE
docker build --target "production" -t $BASE_APPLICATION_IMAGE:production ./docker/$BASE_APPLICATION_IMAGE
docker build --target "test" -t $BASE_APPLICATION_IMAGE:test ./docker/$BASE_APPLICATION_IMAGE

# We must copy the CACERT file into all service dirs to be picked up by each dockerfile
for SERVICE in api classifier flashes special_issues
do 
  cp $SSL_CERT_FILE ./src/"$SERVICE"_service/
done
docker-compose build

if [ $RELEASE == true ]
then
  aws ecr get-login-password --region us-gov-west-1 | docker login --username AWS --password-stdin $ECR_REGISTRY

  # Our API image is just named for the service itself
  docker push $ECR_REGISTRY/$COMMON_PREFIX:$VERSION
  for SERVICE in classifier flashes special_issues
  do
    docker push "$ECR_REGISTRY/$COMMON_PREFIX-$SERVICE-service:$VERSION"
  done
  docker push $ECR_REGISTRY/$COMMON_PREFIX-test:$VERSION
fi
docker rmi $DEPLOY_IMAGE $TEST_IMAGE