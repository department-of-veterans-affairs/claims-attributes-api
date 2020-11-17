#!/usr/bin/env bash
set -euo pipefail
ECR_REGISTRY=533575416491.dkr.ecr.us-gov-west-1.amazonaws.com
IMAGE_NAME=benefits-apis-claims-attributes
IMAGE=$ECR_REGISTRY/$IMAGE_NAME:$VERSION

cp $SSL_CERT_FILE ca-certs.crt
echo "From build.sh - SSL_CERT_FILE: ${SSL_CERT_FILE}, contents w/var: $(cat $SSL_CERT_FILE), raw contents: $(cat ca-certs.crt)"
docker build --build-arg cert_file=ca-certs.crt -t $IMAGE .

if [ $RELEASE == true ]
then
  aws ecr get-login-password --region us-gov-west-1 | docker login --username AWS --password-stdin $ECR_REGISTRY
  docker push $IMAGE
fi
docker rmi $IMAGE