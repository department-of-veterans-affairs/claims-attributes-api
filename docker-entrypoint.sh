#!/bin/sh

set -e

# activate our virtual environment here
echo "Activating virtual environment..."

# if VENV_PATH has been set (e.g. on the server) use it,
# otherwise, ask poetry for it. Then activate our virtual environment
if  [ -z "$VENV_PATH" ]
then
    echo "VENV_PATH not set, using poetry version"
    source "$( poetry env info --path )/bin/activate"
else
    echo "VENV_PATH set to $VENV_PATH, using it"
    source "$VENV_PATH/bin/activate"
fi


# You can put other setup logic here

# Evaluating passed command:
exec "$@"