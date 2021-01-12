#! /usr/bin/env sh
# The adapted taken from https://github.com/tiangolo/uvicorn-gunicorn-docker/blob/master/docker-images/start.sh 

set -e

DEFAULT_MODULE_NAME=app.main
MODULE_NAME=${MODULE_NAME:-$DEFAULT_MODULE_NAME}
VARIABLE_NAME=${VARIABLE_NAME:-app}
export APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}


DEFAULT_GUNICORN_CONF=/gunicorn_conf.py
export GUNICORN_CONF=${GUNICORN_CONF:-$DEFAULT_GUNICORN_CONF}
export WORKER_CLASS=${WORKER_CLASS:-"uvicorn.workers.UvicornWorker"}

# Start Gunicorn
exec authbind gunicorn -k "$WORKER_CLASS" -c "$GUNICORN_CONF" "$APP_MODULE" 