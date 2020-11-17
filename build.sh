#!/usr/bin/env bash
set -euo pipefail
ECR_REGISTRY=533575416491.dkr.ecr.us-gov-west-1.amazonaws.com
IMAGE_NAME=benefits-apis-claims-attributes
IMAGE=$ECR_REGISTRY/$IMAGE_NAME:$VERSION

cp $SSL_CERT_FILE ca-certs.crt
docker build --build-arg COPY_CERTS=1 -t $IMAGE .

if [ $RELEASE == true ]
then
  aws ecr get-login-password --region us-gov-west-1 | docker login --username AWS --password-stdin $ECR_REGISTRY
  docker push $IMAGE
fi
docker rmi $IMAGE