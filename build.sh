#!/usr/bin/env bash
set -euo pipefail
ECR_REGISTRY=533575416491.dkr.ecr.us-gov-west-1.amazonaws.com
IMAGE_NAME=benefits-apis-claims-attributes
TEST_IMAGE_NAME=$TEST_IMAGE-test
DEPLOY_IMAGE=$ECR_REGISTRY/$IMAGE_NAME:$VERSION
TEST_IMAGE=$ECR_REGISTRY/$IMAGE_NAME:$VERSION

# We build two images, one for prod and one for testing, using --target / multi-stage builds 
# as outlined here: https://suda.pl/single-dockerfile-for-testing-and-production/ . 
# For more on our test image and its expectations, see: 
# https://github.com/department-of-veterans-affairs/health-apis-deployer/blob/master/deployment-unit.md
cp $SSL_CERT_FILE cacert.pem
docker build --target "production" -t $IMAGE .
docker build --target "test" -t $TEST_IMAGE .

if [ $RELEASE == true ]
then
  aws ecr get-login-password --region us-gov-west-1 | docker login --username AWS --password-stdin $ECR_REGISTRY
  docker push $IMAGE
  docker push $TEST_IMAGE
fi
docker rmi $IMAGE