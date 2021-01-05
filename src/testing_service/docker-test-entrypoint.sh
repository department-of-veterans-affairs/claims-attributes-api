#!/usr/bin/env bash

# docker-test-entrypoint.sh
# Used by the deployer and deployment unit as described
# here: https://github.com/department-of-veterans-affairs/health-apis-deployer/blob/qa/deployment-unit.md
# Usage: docker run --rm --network host api:testing [regression-test|smoke-test]

set -euo pipefail

usage() {
cat <<EOF
Commands
  smoke-test
  regression-test
$1
EOF
exit 1
}

# Runs Smoke Tests
doSmokeTest() {
  echo "Running Smoke tests..."
  poetry run app/main.py
  RETURN_STATUS=$?
  echo "Return status: $RETURN_STATUS"
  exit "$RETURN_STATUS"
}

# Runs the Regression Test Suite
doRegressionTest() {
  echo "Running Regression tests..."
  poetry run app/main.py
  RETURN_STATUS=$?
  echo "Return status: $RETURN_STATUS"
  exit "$RETURN_STATUS"
}

[ $# == 0 ] && usage "No command specified"
echo "Num: $#, Args: $@ , arg0: $0"
COMMAND=$1
shift
case "$COMMAND" in
  s|smoke-test) doSmokeTest;;
  r|regression-test) doRegressionTest;;
  *) usage "Unknown command: $COMMAND";;
esac

exit 0