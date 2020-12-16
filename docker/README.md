# Docker

This directory consists of two parts:

1. The `va-python-application-base` parent image. This is used to build a parent image that all services inherit from
2. The master `Dockerfile`. This inherits from #1 and is used in `docker-compose` to build all 4 of the constituent CAAPI services. For each the `docker-compose` file passes a different context to use and reference the files directly within that context.

If building locally, build `va-python-application-base` first
